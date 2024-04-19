import sys  # Importerer sys modulet, som giver adgang til systemspecifikke funktioner og variabler.
from PySide6.QtCore import QDateTime, QTimer  # Importerer QDateTime og QTimer klasserne fra PySide6.QtCore modulet.
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QRadioButton, \
    QWidget  # Importerer nødvendige klasser fra PySide6.QtWidgets modulet.


class SkærmForbrugsApp(QMainWindow):  # Definerer en ny klasse, der arver fra QMainWindow.
    def __init__(self):  # Konstruktørmetoden for klassen.
        super().__init__()  # Kalder for superklassen.

        # Initialiserer brugergrænsefladen og variabler.
        self.initUI()
        self.total_skærm_tid = 0
        self.sidste_knap_tryk_tid = None
        self.nuværende_spørgsmål_index = 0
        self.score = 0

        # Opretter en QTimer til pause og en til score, og forbinder dem til deres opdateringsmetoder.
        self.pause_timer = QTimer(self)
        self.pause_timer.timeout.connect(self.opdaterPauseTid)
        self.pause_tid = 0

        self.score_timer = QTimer(self)
        self.score_timer.timeout.connect(self.opdaterScore)

    def initUI(self):  # initialisere brugergrænsefladen.
        self.bredde = 500  # Bredde på vinduet.
        self.højde = 500  # Højde på vinduet.

        # Opretter og konfigurerer knapper og layout.
        self.vis_skærm_forbrug_knap = QPushButton('Vis dit skærmforbrug', self)
        self.vis_skærm_forbrug_knap.clicked.connect(self.visSkærmForbrug)
        self.vis_skærm_forbrug_knap.setGeometry(100, 50, 300, 50)
        self.pause_knap = QPushButton('Pause', self)
        self.pause_knap.clicked.connect(self.togglePause)
        self.pause_knap.setGeometry(100, 0, 100, 50)

        self.pause_tid_label = QLabel('0 sekunder', self)
        self.pause_tid_label.setGeometry(20, 0, 100, 50)

        self.score_label = QLabel('Score: 0', self)
        self.score_label.setGeometry(20, 30, 100, 50)

        self.quiz_knap = QPushButton('Quiz', self)
        self.quiz_knap.clicked.connect(self.visQuiz)
        self.quiz_knap.setGeometry(100, 120, 300, 50)

        self.skærm_forbrug_label = QLabel('Tryk på knappen for at se skærmforbrug', self)
        self.skærm_forbrug_label.setGeometry(100, 200, 300, 50)

        self.quiz_layout = QVBoxLayout()
        self.quiz_widget = QWidget(self)
        self.quiz_widget.setGeometry(100, 260, 300, 150)
        self.quiz_widget.setLayout(self.quiz_layout)

        self.næste_knap = QPushButton('Næste', self)
        self.næste_knap.clicked.connect(self.næsteSpørgsmål)
        self.næste_knap.setGeometry(100, 430, 300, 50)
        self.næste_knap.setEnabled(False)

    def togglePause(self):  # Til at starte og stoppe pause-timeren.
        if not self.pause_timer.isActive():  # Hvis pause-timeren ikke kører.
            self.pause_timer.start(1000)  # Starter pause-timeren med en timeout på 1000 ms (1 sekund).
            self.pause_timer.timeout.connect(
                self.opdaterPauseTid)  # Forbinder timeout-signalet til opdaterPauseTid-metoden.
            self.score_timer.start(1000)  # Starter score-timeren med en timeout på 1000 ms (1 sekund).
        else:  # Hvis pause-timeren kører.
            self.pause_timer.stop()  # Stopper pause-timeren.
            self.score_timer.stop()  # Stopper score-timeren.

    def opdaterPauseTid(self):  # Til at opdatere pause-tiden.
        self.pause_tid += 1 / 2  # Øger pause-tiden med 0.5 sekunder.
        self.pause_tid_label.setText(f'{self.pause_tid} sekunder')  # Opdaterer etiketten med den nye pause-tid.

    def opdaterScore(self):  # Til at opdatere scoren.
        self.score += 1 / 2  # Øger scoren med 0.5. så hver andet sekund er 1 point
        self.score_label.setText(f'Score: {self.score}')  # Opdaterer etiketten med den nye score.

    def opdaterSkærmTid(self):  # Metode til at opdatere skærmens tid.
        nuværende_tid = QDateTime.currentDateTime()  # Henter den aktuelle dato og tid.
        gået_tid = self.start_tid.secsTo(
            nuværende_tid) + self.total_skærm_tid  # Beregner tiden, der er gået siden start_tid.
        self.skærm_forbrug_label.setText(
            f'Skærmforbrug: {gået_tid} sekunder')  # Opdaterer etiketten med skærmforbrugstiden.

    def visSkærmForbrug(self):  # Til at vise skærmforbrug.
        if self.sidste_knap_tryk_tid is None:  # Hvis sidste_knap_tryk_tid er None (dvs. første gang knappen trykkes).
            self.start_tid = QDateTime.currentDateTime()  # Sætter start_tid til den aktuelle dato og tid.
            self.sidste_knap_tryk_tid = self.start_tid  # Gemmer start_tid som sidste_knap_tryk_tid.
            self.opdaterSkærmTid()  # Opdaterer skærmforbrugstiden.
        else:  # Hvis knappen har været trykket før.
            self.total_skærm_tid += self.sidste_knap_tryk_tid.secsTo(
                QDateTime.currentDateTime())  # Beregner tiden, der er gået siden sidste knaptryk.
            self.sidste_knap_tryk_tid = QDateTime.currentDateTime()  # Opdaterer sidste_knap_tryk_tid med den aktuelle dato og tid.
            self.opdaterSkærmTid()  # Opdaterer skærmforbrugstiden.

    def visQuiz(self):  # Til at vise quiz.
        self.opretQuizUI()  # Kalder metoden til at oprette quiz-brugergrænsefladen.
        self.skærm_forbrug_label.hide()  # Skjuler skærmforbrugsetiketten.

    def opretQuizUI(self):  # Til at oprette quiz-brugergrænsefladen.
        self.rydQuizUI()  # Rydder quiz-brugergrænsefladen.
        spørgsmål, svarmuligheder = self.getNæsteSpørgsmål()  # Henter det næste spørgsmål og dets svarmuligheder.

        spørgsmål_label = QLabel(f'Spørgsmål {self.nuværende_spørgsmål_index}: {spørgsmål}',
                                 self)  # Opretter en etiket med spørgsmålet.
        self.quiz_layout.addWidget(spørgsmål_label)  # Tilføjer spørgsmåls etiketten til layoutet.

        for svar in svarmuligheder:  # Gennemgår alle svarmulighederne.
            radio_knap = QRadioButton(svar, self)  # Opretter en radioknap for hver svarmulighed.
            self.quiz_layout.addWidget(radio_knap)  # Tilføjer radioknappen til layoutet.

        self.næste_knap.setEnabled(True)  # Aktiverer næste knappen.

    def rydQuizUI(self):  # Til at rydde quiz-brugergrænsefladen.
        for i in reversed(range(self.quiz_layout.count())):  # Gennemgår alle widgets i layoutet i omvendt rækkefølge.
            self.quiz_layout.itemAt(i).widget().setParent(None)  # Fjerner hver widget fra layoutet.

    def næsteSpørgsmål(self):  # Til at gå til næste spørgsmål.
        self.opretQuizUI()  # Opretter quiz-brugergrænsefladen.

    def getNæsteSpørgsmål(self):  # Metode til at hente det næste spørgsmål og dets svarmuligheder.
        spørgsmål = f'Har du intense trang til skærmtid? {self.nuværende_spørgsmål_index + 1}'  # Opretter et spørgsmål.

        # Definerer hver svarmulighed.
        svarmulighed_1 = 'Aldrig'
        svarmulighed_2 = 'Jævnt'
        svarmulighed_3 = 'Nogle gange'
        svarmulighed_4 = 'Altid'

        # Samler svarmulighederne i en liste.
        svarmuligheder = [svarmulighed_1, svarmulighed_2, svarmulighed_3, svarmulighed_4]

        self.nuværende_spørgsmål_index += 1  # Opdaterer index til det næste spørgsmål. Så at det kommer frem som "Spørgsmål 2" eller 3 eller 4, osv
        return spørgsmål, svarmuligheder  # Returnerer spørgsmålet og svarmulighederne.


if __name__ == '__main__':  # Starter hovedprogrammet.
    app = QApplication(sys.argv)  # Opretter en QApplication-instans.
    ex = SkærmForbrugsApp()  # Opretter en instans af SkærmForbrugsApp-klassen.
    ex.setGeometry(100, 100, ex.bredde, ex.højde)  # Angiver position og størrelse på vinduet.
    ex.setWindowTitle('Applikation med skærmforbrug og quiz')  # Angiver titlen på vinduet.
    ex.show()  # Viser vinduet.
    sys.exit(app.exec())  # Afslutter hovedprogrammet, når vinduet lukkes.

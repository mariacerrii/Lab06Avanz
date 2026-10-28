import flet as ft
from UI.view import View
from model.model import DepositoStrumenti

'''
    CONTROLLER:
    - Funziona da intermediario tra MODELLO e VIEW
    - Gestisce la logica del flusso dell'applicazione
'''

class Controller:
    def __init__(self, view: View, model: DepositoStrumenti):
        self._model = model
        self._view = view

    def get_nome(self):
        return self._model.nome

    def get_responsabile(self):
        return self._model.responsabile

    def set_responsabile(self, responsabile):
        self._model.responsabile = responsabile

    def conferma_responsabile(self, e):
        self._model.responsabile = self._view.input_responsabile.value
        self._view.txt_responsabile.value = f"Responsabile: {self._model.responsabile}"
        self._view.update()

    # Altre Funzioni Event Handler
    # ==================================================
    # FUNZIONE 1: MOSTRA TUTTI GLI STRUMENTI
    # ==================================================
    def mostra_strumenti(self, e):
        # Chiedo al MODEL di recuperare tutti gli strumenti dal database
        strumenti = self._model.get_strumenti()

        # Svuoto la ListView per evitare di duplicare i risultati
        # quando premo più volte il pulsante "Mostra"
        self._view.lista_strumenti.controls.clear()

        # Se il MODEL restituisce None, significa che si è verificato un errore
        if strumenti is None:
            self._view.alert.show_alert(
                "Errore durante il recupero degli strumenti"
            )
            return

        # Scorro tutti gli strumenti recuperati dal database
        for strumento in strumenti:
            # Creo un controllo Text per ogni strumento
            # str() converte l'oggetto Strumento in una stringa
            self._view.lista_strumenti.controls.append(
                ft.Text(str(strumento))
            )

        # Aggiorno l'interfaccia grafica per mostrare i risultati
        self._view.update()

    # ==================================================
    # FUNZIONE 2: CERCA STRUMENTI PER TIPO
    # ==================================================
    def cerca_strumenti(self, e):
        # Recupero il testo inserito dall'utente
        # .value legge il contenuto del TextField
        # .strip() elimina eventuali spazi iniziali e finali
        tipo = self._view.input_tipo_strumento.value.strip()

        # Controllo che l'utente abbia inserito un tipo
        if tipo == "":
            self._view.alert.show_alert(
                "Inserire un tipo di strumento"
            )
            return

        # Chiedo al MODEL di cercare gli strumenti del tipo indicato
        strumenti = self._model.cerca_strumenti_per_tipo(tipo)

        # Svuoto la ListView prima di mostrare i nuovi risultati
        self._view.lista_strumenti_ricerca.controls.clear()

        # Gestisco un eventuale errore nella lettura dal database
        if strumenti is None:
            self._view.alert.show_alert(
                "Errore durante la ricerca"
            )
            return

        # Se la lista è vuota, nessuno strumento corrisponde al tipo cercato
        if len(strumenti) == 0:
            # Mostro un messaggio nella ListView
            self._view.lista_strumenti_ricerca.controls.append(
                ft.Text("Nessuno strumento trovato")
            )
        else:
            # Se sono stati trovati strumenti, li visualizzo uno alla volta
            for strumento in strumenti:
                # Aggiungo ogni strumento alla ListView
                self._view.lista_strumenti_ricerca.controls.append(
                    ft.Text(str(strumento))
                )

        # Aggiorno l'interfaccia grafica
        self._view.update()
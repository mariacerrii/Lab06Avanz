from database.DB_connect import get_connection
from model.strumento import Strumento
from model.prestito import Prestito

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        self._nome = nome
        self._responsabile = responsabile

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome):
        self._nome = nome

    @property
    def responsabile(self):
        return self._responsabile

    @responsabile.setter
    def responsabile(self, responsabile):
        self._responsabile = responsabile

    def get_strumenti(self) -> list[Strumento] | None:
        conn = get_connection()
        if conn is None:
            print("ERRORE: connessione al database non riuscita")
            return None

        risultati = []
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                        SELECT *
                        FROM strumento
                        """

            cursor.execute(query)
            for row in cursor:
                risultati.append(Strumento(**row))

            cursor.close()
            return risultati

        except Exception as e:
            print(f"Errore durante il recupero degli strumenti: {e}")
            return None

        finally:
            conn.close()

    def cerca_strumenti_per_tipo(self, tipo) -> list[Strumento] | None:
        conn = get_connection()
        if conn is None:
            return None

        risultati = []

        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT *
                FROM strumento
                WHERE tipo = %s
                """

            cursor.execute(query, (tipo,))
            for row in cursor:
                risultati.append(Strumento(**row))

            cursor.close()
            return risultati

        except Exception as e:
            print(f"Errore durante la ricerca degli strumenti: {e}")
            return None

        finally:
            conn.close()

def filtra_dizionario(dizionario, parola_da_cercare):
    """
    Filtra un dizionario cercando una parola nei valori delle chiavi che sono liste di oggetti con 
    i campi 'assenze', 'eventi', 'uscite', 'note'.
    
    :param dizionario: dict, il dizionario da filtrare
    :param parola_da_cercare: str, la parola da cercare nei campi 'testo'
    :return: dict, un nuovo dizionario con i valori filtrati
    """
    parola_da_cercare = parola_da_cercare.lower()  # Per rendere la ricerca case-insensitive
    dizionario_filtrato = {}
    
    for chiave, lista in dizionario.items():
        if isinstance(lista, list):  # Verifica che il valore sia una lista
            # Filtra gli oggetti della lista il cui campo 'testo' contiene la parola da cercare
            lista_filtrata = [
                oggetto for oggetto in lista 
                if parola_da_cercare in oggetto.get('assenze', '').lower() + 
                                        oggetto.get('uscite', '').lower() +
                                        oggetto.get('eventi', '').lower() +
                                        oggetto.get('note', '').lower()
            ]
            if lista_filtrata:  # Aggiungi alla chiave solo se ci sono corrispondenze
                dizionario_filtrato[chiave] = lista_filtrata 
    
    return dizionario_filtrato


# Esempio di utilizzo
dizionario = {
    "chiave1": [{"testo": "Questo è un esempio"}, {"testo": "Prova con Python"}],
    "chiave2": [{"testo": "Un altro esempio di ricerca"}, {"altro_campo": "Non considerare"}],
    "chiave3": [{"testo": "Python è potente"}],
}

parola = "python"
risultato = filtra_dizionario(dizionario, parola)
print(risultato)

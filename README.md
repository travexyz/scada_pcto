---

# Docker Container Manager GUI

Il **Docker Container Manager GUI** è un progetto sviluppato in Python che consente di gestire in modo semplice e intuitivo i container Docker, avvalendosi di un’interfaccia grafica basata sul toolkit **Tkinter**.

---

## 📌 Finalità del progetto

Il progetto si propone di offrire uno strumento pratico e immediato per:

* Avviare container Docker in modalità *detached*.
* Esporre in modo automatico le porte dei container.
* Gestire l’arresto e la rimozione dei container creati.
* Offrire un’interfaccia grafica user-friendly per agevolare la gestione dei container, anche a utenti meno esperti.

---

## ⚙️ Componenti principali

### 1️⃣ `ContainerManager`

La classe `ContainerManager` è il nucleo operativo del progetto. Le sue principali responsabilità sono:

* **Creazione dei container**: crea container a partire dall’immagine `nginx:latest`, assegnando nomi univoci e configurando la porta interna 80 su una porta esterna incrementale (a partire da un valore di base configurabile, di default `6000`).
* **Gestione dei container**: mantiene un elenco dei container attivi, che possono essere avviati, fermati e rimossi in modo sicuro.
* **Sincronizzazione**: implementa un meccanismo di sincronizzazione basato su `threading.Lock`, per garantire che le operazioni di gestione non vengano eseguite in modo concorrente.
* **Interazione con la GUI**: aggiorna l’interfaccia grafica per comunicare all’utente lo stato delle operazioni.

### 2️⃣ `GUI_Manager`

La classe `GUI_Manager` si occupa dell’interfaccia utente. Le sue principali caratteristiche sono:

* **Input semplice**: consente di inserire il numero di container da avviare.
* **Pulsanti di controllo**: mette a disposizione comandi per avviare e arrestare tutti i container.
* **Messaggi informativi**: fornisce un feedback visivo sullo stato delle operazioni (ad esempio, l’avvio o l’arresto dei container).
* **Reattività**: le operazioni di gestione vengono eseguite in thread separati, così l’interfaccia grafica rimane sempre reattiva.

---

## 🏗️ Funzionamento del sistema

1. **Configurazione della porta di partenza**
   La porta iniziale per l’esposizione esterna dei container è impostata a `6000`, ma può essere modificata al momento dell’istanza del `ContainerManager`.

2. **Avvio dei container**
   L’utente inserisce nella GUI il numero desiderato di container e avvia il processo tramite l’apposito pulsante. Ogni container viene avviato in modalità *detached* e assegnato a una porta incrementale (`6000`, `6001`, …).

3. **Arresto e rimozione dei container**
   Tramite un pulsante dedicato, l’utente può arrestare e rimuovere in modo sicuro tutti i container creati dall’applicazione.

4. **Conferma delle operazioni**
   Le operazioni di avvio richiedono una conferma tramite finestra di dialogo, per evitare avvii accidentali.

---

## 🚀 Modalità di esecuzione

Per eseguire l’applicazione, è necessario disporre di:

* **Python 3**
* **Docker** in esecuzione sul sistema

È sufficiente eseguire lo script principale:

```bash
python your_script.py
```

Al termine, si aprirà la finestra dell’interfaccia grafica, pronta per la gestione dei container.

![input](https://github.com/user-attachments/assets/cb1a1168-dd86-4f9f-a7e9-823fe762124d)

Mostrando anche lo stato attuale dei container

![container](https://github.com/user-attachments/assets/d7f44087-4379-4540-afea-67e68b20f837)


La schermata sparirà una volta rimossi i container

![kill](https://github.com/user-attachments/assets/43a38b74-892d-450b-8beb-7f55935235a4)


---

## 🔎 Considerazioni finali

* L’applicazione si basa sull’immagine `nginx:latest`. In assenza dell’immagine, Docker provvederà a scaricarla automaticamente.
* I container creati sono nominati in modo univoco (`cont_0`, `cont_1`, ecc.) e assegnati a porte incrementali, per evitare conflitti e garantire la tracciabilità.

---

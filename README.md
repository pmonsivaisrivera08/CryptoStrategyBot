📊 Trading Bot - Technical Strategies on Binance

This project is an interactive trading bot that connects to the Binance API to scan and analyze cryptocurrencies in real time using different technical analysis strategies.

The bot is built with an interactive console menu, allowing users to easily select and execute multiple trading tools.

⚡ Main Features

When running the bot, a strategy menu is displayed:

📈 Simple Moving Averages (SMA)
Calculates and processes simple moving averages of closing prices.

📉 Exponential Moving Averages (EMA)
Triple EMA crossover strategy (10, 20, 30 periods).
Continuously scans tickers for signals.

🔄 RSI (Relative Strength Index)
Applies RSI (14 periods) to tickers and detects overbought/oversold opportunities.

📊 MACD (Moving Average Convergence Divergence)
Runs the MACD strategy and displays final results.

🎯 Bollinger Bands
Scans tickers with Bollinger Bands (20, 2).
Stops scanning once a signal is detected.

🚪 Exit
Terminates the bot execution.

🔄 Program Flow

Clears the screen.

Displays the main menu.

User selects a strategy.

The bot fetches data from Binance and executes the chosen strategy.

After processing, it returns to the menu until the user decides to exit.

🛠️ Technologies Used

Python 3

Binance API (python-binance)

Pandas

OS / Time

🚀 Usage

Clone this repository:

git clone https://github.com/your-username/tradingbot.git
cd tradingbot


Install dependencies:

pip install python-binance pandas


Add your Binance API keys in the file:

API_KEY = "YOUR_API_KEY"
API_SECRET = "YOUR_API_SECRET"


Run the bot using Jupyter Notebook or directly with Python.

⚠️ Disclaimer

This bot is for educational purposes only.
It is not optimized for live trading and does not guarantee profitability.
Use it at your own risk.

__________________________________________________________________________________

📊 Trading Bot - Estrategias Técnicas en Binance

Este proyecto es un bot de trading interactivo que se conecta con la API de Binance para escanear y analizar criptomonedas en tiempo real mediante diferentes estrategias de análisis técnico.

El bot está diseñado con un menú interactivo en consola, que permite seleccionar entre varias herramientas de trading y ejecutarlas de manera sencilla.

⚡ Funcionalidades principales

Al ejecutar el bot, se muestra un menú de estrategias:

📈 Medias Móviles Simples (SMA)
Calcula y procesa medias móviles simples de los precios de cierre.

📉 Medias Móviles Exponenciales (EMA)
Estrategia de cruce triple de EMAs (10, 20, 30 periodos).
Escanea continuamente los tickers en busca de señales.

🔄 RSI (Índice de Fuerza Relativa)
Aplica RSI de 14 periodos sobre los tickers y detecta oportunidades de sobrecompra o sobreventa.

📊 MACD (Convergencia/Divergencia de Medias Móviles)
Ejecuta la estrategia MACD y muestra el procesamiento final.

🎯 Bandas de Bollinger
Escanea tickers con Bandas de Bollinger (20, 2).
Se detiene al encontrar una señal.

🚪 Salir
Finaliza la ejecución del bot.

🔄 Flujo del programa

Se limpia la pantalla.

Se muestra el menú principal.

El usuario selecciona una estrategia.

El bot procesa los datos de Binance y ejecuta la estrategia seleccionada.

Una vez finalizado, regresa al menú hasta que el usuario decida salir.

🛠️ Tecnologías utilizadas

Python 3

Binance API (python-binance)

Pandas

OS / Time

🚀 Uso

Clona este repositorio:

git clone https://github.com/tu-usuario/tradingbot.git
cd tradingbot


Instala las dependencias necesarias:

pip install python-binance pandas


Agrega tus claves de la API de Binance en el archivo:

API_KEY = "TU_API_KEY"
API_SECRET = "TU_API_SECRET"


Ejecuta el bot desde Jupyter Notebook o directamente en Python.

⚠️ Nota importante

Este bot tiene fines educativos.
No está optimizado para trading en vivo ni garantiza rentabilidad.
Úsalo bajo tu propia responsabilidad.

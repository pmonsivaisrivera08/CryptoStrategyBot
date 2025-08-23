from binance.client import Client
from binance.enums import *
import pandas as pd
import os
import time

API_KEY = ""
API_SECRET = ""

client = Client(API_KEY,API_SECRET, tld = 'com')

def obtener_todos_los_tickers_binance():
    lista_tickers = client.get_all_tickers()
    
    for ticker in lista_tickers:
        symbol = ticker['symbol']
        price = ticker['price']
    
        print("Simbolo: " + symbol + "Precio:" + price)


def SMA_INTERVALO_1HS(periodo,ticker):
    lista_precios_cierre = []
    
    data_historical = client.get_historical_klines(ticker,Client.KLINE_INTERVAL_1HOUR,'250 hour ago UTC')
    
    #print("cantidad de velas: ",len(data_historical))
    
    sumatoria = 0
    
    if len(data_historical) == 250:
    
        #print("se obtuvieron los datos correctamente")
    
        for i in range((250 - periodo), 250):
            #print(data_historical[i])
        
            sumatoria += float(data_historical[i][4])
    
        sma=sumatoria/periodo
        #print("SMA: " + ticker + " Periodo:" + str(periodo) + ":" + str(sma))
        return(sma)

    else:
        print("no se pudo obtener el historial de velas")


#sma4 = SMA_INTERVALO_1HS(4,'BTCUSDT')
#sma9 = SMA_INTERVALO_1HS(9,'BTCUSDT')
#sma18 = SMA_INTERVALO_1HS(18,'BTCUSDT')

#if sma4 > sma9 and sma4 > sma18:
    #print("se esta cumpliendo la estrategia triple cruce SMA 4 9 18")
#else:
    #print("no se esta cumpliendo la estrategia triple cruce SMA 4 9 18")

def EMA_INTERVALO_1HS(periodo,ticker):
    
    lista_precios_cierre = []
    ema = []
    
    data_historical = client.get_historical_klines(ticker,Client.KLINE_INTERVAL_1HOUR,'250 hour ago UTC')
    
    #print("cantidad de velas:", len(data_historical))
    
    sma = SMA_INTERVALO_1HS(periodo,ticker)
    ema.append(sma)
    #print("primer valor emas:", ema)
    
    if len(data_historical) == 250:
        #print("se obtuvieron los datos correctamente")
        
        for i in range(len(data_historical)):
            lista_precios_cierre.append(float(data_historical[i][4]))
        
        #print("cantidad de velas para periodo:", len(lista_precios_cierre[periodo:]))
        for price in lista_precios_cierre[periodo:]:
            ema.append( (price * (2/(periodo + 1 ) ) ) + ema[-1] * (1 -(2 / (periodo + 1) ) ) )
        
        #print("cantidad de elementos: ", len(ema))
        #for i in ema:
            #print(i)
        
        ema_valor = round(ema.pop(),3)
        
        #print("EMA:" + ticker + " Periodo:" + str(periodo) + " : " + str(ema_valor))
        
        return(ema_valor)
    
    else:
        print("no se pudo obtener el historial de velas")


#Puedes cambiar el 10 por el período que desees y SOLUSDT por la criptomoneda que quieras de Binance.
#You can change 10 to any period you want and SOLUSDT to any cryptocurrency you want from Binance.

#Estrategia Triple Cruce con ema
#Triple EMA Crossover


   # ema10 = EMA_INTERVALO_1HS(10,"BTCUSDT")
    #ema20 = EMA_INTERVALO_1HS(20,"BTCUSDT")
    #ema30 = EMA_INTERVALO_1HS(30,"BTCUSDT")


    #if ema10 > ema20 and ema10 > ema30:
        #print("\nAlerta!!!")
        #print("Ticker: " + ticker + "EMA RAPIDA POR ENCIMA DE LAS OTRAS 2 - POSIBLE MOV. ALCISTA\n")
    
    #else:
        #print("\n No se esta culpiendo la estrategia ")



#Calculo RSI grafico 1 hora, dado periodo y ticker
#RSI calculation for 1-hour chart, given period and ticker

def RSI_INTERVALO_1HS(periodo,ticker):
    lista_precios_cierre = []
    data_historical = client.get_historical_klines(ticker,Client.KLINE_INTERVAL_1HOUR,'250 hour ago UTC')
    
    #print("Cantidad de velas: ",len(data_historical))
    
    if len(data_historical) ==250:
        print("se obtuvieron los datos correctamente")
        
        for i in range(len(data_historical)):
            lista_precios_cierre.append(float(data_historical[i][4]))
        
        dic_lpc = {"precios_cierre": lista_precios_cierre}
        
        dataFrame = pd.DataFrame(dic_lpc)
        
        #print(dataFrame)
        
        diferencia = dataFrame["precios_cierre"].diff(1)
        #print(diferencia)
        
        positivos = diferencia.copy()
        negativos = diferencia.copy()
        
        positivos[positivos<0] = 0
        negativos[negativos>0] = 0
        
        #print(positivos)
        #print(negativos)
        
        ema_positivos = positivos.ewm(com = (periodo-1), adjust = False).mean()
        ema_negativos = abs(negativos.ewm(com = (periodo-1), adjust = False).mean())
        
        rs = ema_positivos/ ema_negativos
        
        rsi = 100 - (100/(rs+1))
        #print(rsi)
        rsi_valor = round(rsi.iloc[-1],2)
        
        print("RSI: ", rsi_valor)
        
        return rsi_valor
                        
        
           
    else:
        print("no se obtuvieron los datos correctamente")


#Estrategia RSI
#RSI

def estrategia_rsi(periodo,ticker):
    print("Ticker Analizado: ", ticker)
    rsi = RSI_INTERVALO_1HS(periodo,ticker)
    
    if rsi != None:
        
        #SI EL VALOR  DEL RSI ES MENOR A 30 ENTONCES ESTA EN SOBREVENTA ENTONCES HAY POSIBLE MOVIMIENTO ALCISTA
        if rsi < 30:
            print("\nAlerta!!!")
            print("Ticker: " + ticker + " RSI menor al nivel 30 (sobreventa) - POSIBLE MOV. ALCISTA\n")
            
            
        #SI EL VALOR DEL RSI ES MAYOR A 70 ENTONCES ESTA EN SOBRECOMPRA ENTONCES HAY UN POSIBLE MOVIMIENTO BAJISTA
        if rsi > 70:
            print("\nAlerta!!!")
            print("Ticker: " + ticker + "RSI mayor al nivel 70 (SOBRECOMPRA) - POSIBLE MOV. BAJISTA\n")
        return True
    else:
        print("No SE PUDO VERIFICAR LA ESTRATEGIA\n")
        return False


#________________________Crear dataframe
#Create Dataframe


def crearDataframe(ticker):
    lista_precios_cierre = []
    data_historical = client.get_historical_klines(ticker,Client.KLINE_INTERVAL_1HOUR,'250 hour ago UTC')
    
    if len(data_historical) > 201:
        #print("se obtuvieron los datos correctamente")
        
        for i in range(len(data_historical)):
            lista_precios_cierre.append(float(data_historical[i][4]))
        
        dic_lpc = {"precios_cierre":lista_precios_cierre}
        
        dataFrame = pd.DataFrame(dic_lpc)
        
        return True,dataFrame
    else:
        print("No se obtuvieron los datos correctamente")
        return False, None



re, df = crearDataframe("BTCUSDT")


#print(df)


#MACD a partir de los periodos 1 y2, y signal a partir de la periodo 3

def MACD_INTERVALO_1HS(periodo1,periodo2,periodo3,ticker):
    
    resultado, dataframe = crearDataframe(ticker)
    
    if resultado == True:
        
        #Calculo MACD
        
        exp1 = dataframe.ewm(span=periodo1, adjust=False).mean()
        exp2 = dataframe.ewm(span=periodo2, adjust=False).mean()
        
        macd = exp1 - exp2
        
        print(macd)
        #calculo signal
        
        signal = macd.ewm(span=periodo3, adjust=False).mean()
        print(signal)
        
        macd_valor = round(macd.loc[249,"precios_cierre"],4)
        signal_valor = round(signal.loc[249,"precios_cierre"],4)
        
        print("MACD: ", macd_valor)
        print("SIGNAL:", signal_valor)
        
        return macd_valor,signal_valor
    
    else:
        print("no se pudieron obtener los datos")
        
        return None,None


#La primera fila es el número del medio del MACD en TradingView, y la segunda fila es el tercer número en TradingView.
#The first row is the middle number of the MACD on TradingView, and the second row is the third number on TradingView.

#ESTRATEGIA MACD

#macd, signal = MACD_INTERVALO_1HS(12,26,9,"SOLUSDT")

#if macd != None and signal != None:
    #verificamos estrategia
    #if macd > signal:
        #print("MACD POR ENSIMA DE SIGNAL - POSIBLE MOV. ALCISTA")
    #else:
        #print("MACD POR DEBAJO DE SIGNAL - POSIBLE MOV. BAJISTA")
#else:
    #print("No se pudo verificar la estrategia")


#INDICADOR TECNICO BANDAS BOLLINGER --------> valores de precio de cierre, banda superior, banda media y banda inferior


def BANDASBOLLINGER_INTERVALO_1HS(periodo, desviacion_estandar, StdDev, ticker):
    resultado, dataframe = crearDataframe(ticker)
    if resultado == True:
        #agregar columnas para SMA, desviacion estandar y las bandas superior e inferior
        
        dataframe['SMA'] = dataframe['precios_cierre'].rolling(periodo).mean()
        dataframe['Std'] = dataframe['precios_cierre'].rolling(desviacion_estandar).std()
        
        #Calculo de bandas de bollinger
        
        dataframe['BSuperior'] = dataframe['SMA'] + (StdDev * dataframe['Std'])
        dataframe['BInferior'] = dataframe['SMA'] - (StdDev * dataframe['Std'])
        
        #print(dataframe)

        #retornar valores precio cierre, banda media, banda superior y banda inferior
        precios_cierre = round(dataframe.loc[249, 'precios_cierre'], 4)
        banda_superior = round(dataframe.loc[249, 'BSuperior'], 4)
        banda_media = round(dataframe.loc[249, 'SMA'], 4)
        banda_inferior = round(dataframe.loc[249, 'BInferior'], 4)
        
        #print("precio cierre: ", precios_cierre)
        #print("banda superior: ", banda_superior)
        #print("banda media: ", banda_media)
        #print("banda inferior: ", banda_inferior)

        return precios_cierre, banda_superior, banda_media, banda_inferior
    
    else:
        print("no se pudieron obtener los datos")



def estrategia_bandas_bollinger(periodo,desviacion_estandar, StdDev, ticker):
    print("TICKER ANALIZANDO: ", ticker)
    precios_cierre, banda_superior, banda_media, banda_inferior = BANDASBOLLINGER_INTERVALO_1HS(periodo,desviacion_estandar,StdDev,ticker)

    if precios_cierre != None and banda_superior != None and banda_media != None and banda_inferior != None:
    #verificamos estrategia
    
    #si el precio rompe hacia arriba la banda supeior
        if precios_cierre > banda_superior:
            print("\nALERTA!!\n")
            print("Ticker: "+ ticker + "precio por ensima de la banda supeior - posible mov. BAJISTA\n")
            return True
    #si el precio rompe hacia abajo la banda inferior
        if precios_cierre < banda_inferior:
            print("\nALERTA!!\n")
            print("Ticker: "+ ticker + "precio por debajo de la banda inferior - posible mov. ALCISTA")
            return True
    #si el precio rompe hacia arriba la banda media
        if precios_cierre > banda_media:
            print("\nALERTA!!\n")
            print("Ticker: "+ ticker + "precio por arriba de la banda media - posible mov. ALCISTA")
            return True
    #Si el precio rompe por debajo la banda media
        if precios_cierre < banda_media:
            print("\nALERTA!!\n")
            print("Ticker: "+ ticker + "precio por debajo de la banda media - posible mov. BAJISTA")
            return True

    


    else:
        print("\nNo se pudo verificar la estrategia")
        return False


#BANDASBOLLINGER_INTERVALO_1HS(20,20,2,"SOLUSDT")

def opcion1():
    print("Estrategia Medias Moviles Simples")
    print("\nProcesando Estrategia")
    print("Procesamiento finalizado")
    input("\nPresione ENTER para regresar al menu")
    os.system("cls")
    
def opcion2():
    print("Estrategia Medias Moviles Exponenciales")
    print("\nProcesando Estrategia")
    
   
    while True:
        for ticker in listado_tickers:
             res = estrategia_cruce_triple_emas(10,20,30,ticker)
             if res == True:
                 time.sleep(5)

            
           
    
def opcion3(listado_tickers):
    print("Estrategia RSI")
    print("\nProcesando estrategia")
    
    while True:
        for ticker in lista_tickers:
            res = estrategia_rsi(14,ticker)
            if res == True:
                time.sleep(5)
 
    
def opcion4():
    print("Estrategia MACD")
    print("\nProcesando Estrategia")
    print("Procesamiento finalizado")
    input("\nPresione ENTER para regresar al menu")
    os.system("cls")

def opcion5(listado_tickers):
    print("Estrategia BANDAS DE BOLLINGER")
    print("\nProcesando Estrategia\n")
    
    escanear = 1
    while escanear ==1:
        for ticker in listado_tickers:
            res = estrategia_bandas_bollinger(20,20,2,ticker)
            if res == True:
                escanear = 0
                break
    
    
    
    
    print("Procesamiento finalizado")
    input("\nPresione ENTER para regresar al menu")
    os.system("cls")



def mostrar_menu():
    menu = {
    1: "Medias Moviles Simples SMA",
    2: "Medias Moviles Exponenciales EMA",
    3: "RSI",
    4: "MACD",
    5: "BANDAS DE BOLLINGER",
    0: "SALIR"
    }
    for opcion in menu.keys():
        print(opcion, "-", menu[opcion])



def escanear(tickers):
    os.system("cls")
    bucle = 1
    
    while bucle ==1:
        
        print("Seleccione una estrategia\n")
        # mostrar opciones menu
        mostrar_menu()
        #SOLICITAR INGRESO DE OPCION
        op = input("\nIngrese una opcion: ")
        
        #verificar opcion
        if op == "1":
            os.system("cls")
            opcion1()
        elif op == "2":
            os.system("cls")
            opcion2(tickers)
        elif op == "3":
            os.system("cls")
            opcion3(tickers)
        elif op == "4":
            os.system("cls")
            opcion4()
        elif op == "5":
            os.system("cls")
            opcion5(tickers)
        elif op == "0":
            
            bucle == 0
            print("Ejecucion del bot escaneador finalizada.")

        else:
            os.system("cls")
            print("Opcion invalidad. Las posibles opciones son del 0 al 5.\n")



#Puedes colocar los tickers que desees, siempre y cuando estén en Binance, o también puedes usar la función obtener_todos_los_ticker_binance si deseas todos los tickers/criptomonedas
#You can place the tickers you want as long as they are on Binance, or you can also use the function obtener_todos_los_ticker_binance if you want all the tickers/cryptocurrencies.

tickers = ["ETHUSDT", "USDCUSDT", "BTCUSDT", "SOLUSDT", "ETHUSDC"]

escanear(tickers)

#Estrategia con bandas de bollinger
#Verifica la estrategia definida, devolviendo:
#True si cumple alguna de las condiciones de compra/long o venta/short
#False si no cumple ninguna

def estrategia_bandas_bollinger(periodo,desviacion_estandar, StdDev, ticker):
    precios_cierre, banda_superior, banda_media, banda_inferior = BANDASBOLLINGER_INTERVALO_1HS(periodo,desviacion_estandar,StdDev,ticker)

    if precios_cierre != None and banda_superior != None and banda_media != None and banda_inferior != None:
    #verificamos estrategia
    
    #si el precio rompe hacia arriba la banda supeior
        if precios_cierre > banda_superior:
            print("ALERTA!!\n")
            print("Ticker: "+ ticker + "precio por ensima de la banda supeior - posible mov. BAJISTA\n")
            return True
    #si el precio rompe hacia abajo la banda inferior
        if precios_cierre < banda_inferior:
            print("ALERTA!!\n")
            print("Ticker: "+ ticker + "precio por debajo de la banda inferior - posible mov. ALCISTA")
            return True
    #si el precio rompe hacia arriba la banda media
        if precios_cierre > banda_media:
            print("ALERTA!!\n")
            print("Ticker: "+ ticker + "precio por arriba de la banda media - posible mov. ALCISTA")
            return True
    #Si el precio rompe por debajo la banda media
        if precios_cierre < banda_media:
            print("ALERTA!!\n")
            print("Ticker: "+ ticker + "precio por debajo de la banda media - posible mov. BAJISTA")
            return True

    


    else:
        print("No se pudo verificar la estrategia")
        return False


def estrategia_cruce_triple_emas(periodo1,periodo2,periodo3,ticker):
    print("Ticker analizando: " , ticker)
    verifica = False
    
    ema1 = EMA_INTERVALO_1HS(periodo1,ticker)
    ema2 = EMA_INTERVALO_1HS(periodo2,ticker)
    ema3 = EMA_INTERVALO_1HS(periodo3,ticker)

    #se cumple condicion alcista

    if ema1 > ema2 and ema1 > ema3:
        print("\nAlerta!!!")
        print("Ticker: " + ticker + " EMA RAPIDA POR ENCIMA DE LAS OTRAS 2 - POSIBLE MOV. ALCISTA\n")
        verifica = True
        return verifica

    #se cumple condicion bajista
    if ema1 < ema2 and ema1 < ema3:
        print("\nAlerta!!!")
        print("Ticker: " + ticker + " EMA RAPIDO POR DEBAJO DE LAS OTRAS 2 - POSIBLE MOV. BAJISTA\n")
        verifica = True
        return verifica
    
    else:
        #print("\nNO SE PUDO VERIFICAR LA ESTRATEGIA ")
        return verifica




from tkinter import *
from matplotlib import pyplot as plt
import numpy as np

def fechar_graf():

    plt.close('all')

    main.destroy()

#BR: cálculo A + B -> C + D; batelada; reação irreversível

def BR():

    # Calcular tempo 1 = A + B -> C + D Batelada, Reator Ideal, V cte

    # Armazenar os valores inseridos em "Entry"
    xa = xa_entry.get()
    k = k_entry.get()
    Ca = Ca_entry.get()

    # Check de todos os possíveis inputs que crasharia o programa:
    # Qualquer coisa ao invés de número [OK]
    # Xa = 1 e Xa, K e Ca = 0 [OK]
    # Permitir usar a vírgula como separador decimal [OK]
    try:
        xa = float(xa.replace(",","."))
        try:
            k = float(k.replace(",","."))
            try:
                Ca = float(Ca.replace(",","."))
                if xa == 0 or k == 0 or Ca == 0:
                    raise RuntimeError
                elif xa > 1 or xa <= 0:
                    raise TypeError
                else:
                    try:
                        t = (xa / (1 - xa)) / (k * Ca)
                        t = round(t, 2)
                        if t >= 0:
                            resposta_label["text"] = f"O tempo necessário é de {t} horas."

                            # Habilitar botão "Gerar Gráfico"
                            botao_grafico["state"] = NORMAL
                        else:
                            raise TypeError

                    except ValueError as e:
                        resposta_label["text"] = str(e)
                        # Desabilitar botão "Gerar Gráfico" em caso de erro
                        botao_grafico["state"] = DISABLED

                    # Resultado das possíveis exceções
                    except ZeroDivisionError:
                        if xa >= 1:
                            resposta_label["text"] = "Xa deve ser maior que 0 e menor que 1."
                            botao_grafico["state"] = DISABLED
                        elif k <= 0:
                            resposta_label["text"] = "K deve ser maior que 0."
                            botao_grafico["state"] = DISABLED
                        else:
                            resposta_label["text"] = "A concentração inicial de A deve ser maior que 0."
                            botao_grafico["state"] = DISABLED
            except ValueError:
                resposta_label["text"] = "Favor inserir apenas números."
                botao_grafico["state"] = DISABLED
            except RuntimeError:
                resposta_label["text"] = "Favor inserir apenas números maiores que 0"
                botao_grafico["state"] = DISABLED
            except TypeError:
                resposta_label["text"] = "Xa deve ser maior que 0 e menor que 1."
                botao_grafico["state"] = DISABLED
        except ValueError:
            resposta_label["text"] = "Favor inserir apenas números."
            botao_grafico["state"] = DISABLED
    except ValueError:
        resposta_label["text"] = "Favor inserir apenas números."
        botao_grafico["state"] = DISABLED


def graf_BR():

    try:
        xa = xa_entry.get()
        xa = float(xa.replace(",", "."))
        k = k_entry.get()
        k = float(k.replace(",", "."))
        Ca = (Ca_entry.get())
        Ca = float(Ca.replace(",", "."))

        # Ajuste de curva
        if Ca == 1:
            # Equação Logarítmica para ser possível plotar o gráfico com Ca == 1
            # Testar implementação com Ca == 1 com np.linspace(0.9, Ca, num=10) sem equação logarítmica
            concentracoes_iniciais = np.linspace(1e-1, Ca, num=10)
            tempos = (xa / (1 - xa)) / (k * concentracoes_iniciais)
            plt.scatter(concentracoes_iniciais, tempos)
            plt.xlabel("Concentração Inicial de A [mol/L]")
            plt.ylabel("Tempo necessário [horas]")
            plt.title("Relação entre Concentração Inicial e Tempo")
            z = np.polyfit(np.log(concentracoes_iniciais), tempos, 1)
            p = np.poly1d(z)
            plt.plot(concentracoes_iniciais, p(np.log(concentracoes_iniciais)), color='red')
            equacao_label = f"Equação: t = {z[0]:.4f}ln(Ca0) + {z[1]:.4f}"
        else:
            concentracoes_iniciais = np.linspace(1, Ca, num=10)
            tempos = (xa / (1 - xa)) / (k * concentracoes_iniciais)
            plt.scatter(concentracoes_iniciais, tempos)
            plt.xlabel("Concentração Inicial de A [mol/L]")
            plt.ylabel("Tempo necessário [horas]")
            plt.title("Relação entre Concentração Inicial e Tempo")
            z = np.polyfit(concentracoes_iniciais, tempos, 1)
            p = np.poly1d(z)
            plt.plot(concentracoes_iniciais, p(concentracoes_iniciais), color='red')
            equacao_label = f"Equação: t = {z[0]:.4f}Ca0 + {z[1]:.4f}"

        # Posição do texto da equação
        plt.text(0.1, 0.9, equacao_label, transform=plt.gca().transAxes)
        # Atualização Simultânea do Gráfico
        plt.show()
        plt.ion()
    except ValueError:
        resposta_label["text"] = "Erro ao gerar o gráfico. Verifique as entradas."


def jan_BR():
    janela = Toplevel(main)
    janela.focus_set()
    janela.resizable(False,False)
    janela.title("Cálculo Cinética Aplicada à Reatores")

    # Título da janela
    texto = Label(janela, text="Calcule o tempo necessário para a reação A+B->C+D")
    texto.grid(column=0, row=0, padx=50, pady=10)

    # Fornecer xa
    texto_xa = Label(janela, text="Forneça a fração de A que reagiu (Xa)")
    texto_xa.grid(column=0, row=1)
    global xa_entry
    xa_entry = Entry(janela, bd=2)
    xa_entry.grid(column=0, row=2, padx=50, pady=10)
    xa_entry.focus_set()

    # Fornecer k
    texto_k = Label(janela, text="Forneça a velocidade específica da reação (K) [L/mol.h]")
    texto_k.grid(column=0, row=3)
    global k_entry
    k_entry = Entry(janela, bd=2)
    k_entry.grid(column=0, row=4, padx=50, pady=10)

    # Fornecer Ca
    texto_ca = Label(janela, text="Forneça a Concentração Inicial de A [mol/L]")
    texto_ca.grid(column=0, row=5)
    global Ca_entry
    Ca_entry = Entry(janela, bd=2)
    Ca_entry.grid(column=0, row=6, padx=50, pady=10)

    # Apresentar o resultado
    botao_resultado = Button(janela, text="Calcular o Tempo [h]", command=BR)
    botao_resultado.grid(column=0, row=7, padx=50, pady=10)
    botao_resultado["state"] = DISABLED

    global resposta_label
    resposta_label = Label(janela, text="")
    resposta_label.grid(column=0, row=8, padx=50, pady=10)

    # Botão para gerar o gráfico
    global botao_grafico
    botao_grafico = Button(janela, text="Gerar Gráfico", command=graf_BR, state=DISABLED)
    botao_grafico.grid(column=0, row=9, padx=10, pady=10)

    # Verificar campos de entrada para habilitar botão do gráfico
    def verificar_campos(*args):
        if xa_entry.get() and k_entry.get() and Ca_entry.get():
            botao_resultado["state"] = NORMAL
        else:
            botao_resultado["state"] = DISABLED

    xa_entry.bind("<KeyRelease>", verificar_campos)
    k_entry.bind("<KeyRelease>", verificar_campos)
    Ca_entry.bind("<KeyRelease>", verificar_campos)

    # Sair da janela
    Button(janela, text="Sair", command=lambda:[janela.destroy(),main.deiconify(),EQ1.config(state=NORMAL)])\
        .grid(column=0, row=10, padx=50, pady=10)
    janela.protocol("WM_DELETE_WINDOW",lambda:[janela.destroy(),main.deiconify(),EQ1.config(state=NORMAL)])


#CSTR: cálculo para um reator CSTR (em m³)

def CSTR():

    Fa_ra = Fa_ra_entry.get()
    Xa = Xa_entry.get()
    try:
        Fa_ra = float(Fa_ra.replace(",","."))
        try:
            Xa = float(Xa.replace(",","."))
            if Xa > 1 or Xa <= 0:
                raise RuntimeError
            try:
                V = Xa*Fa_ra
                V = round(V,2)
                if V > 0:
                    resposta_label["text"] = f"O volume necessário é de {V} m³."

                    botao_grafico["state"] = NORMAL
                else:
                    resposta_label["text"] = "As entradas deverão ser maiores que 0."
            except ValueError:
                resposta_label["text"] = "Favor insira apenas números"
        except ValueError:
            resposta_label["text"] = "Favor insira apenas números"
        except RuntimeError:
            resposta_label["text"] = "Xa deve ser maior que 0 e menor que 1."
    except ValueError:
        resposta_label["text"] = "Favor insira apenas números"


def graf_CSTR():
    try:
        Fa_ra = Fa_ra_entry.get()
        Fa_ra = float(Fa_ra.replace(",", "."))
        Xa = np.linspace(0.1, 1, num=10)  # Gerar 10 pontos de 0.1 a 1
        V = Xa * Fa_ra  # Calcular V para cada valor de Xa

        # Criar o gráfico
        plt.plot(Xa, V, marker='o', label='Pontos')
        plt.xlabel("Xa")
        plt.ylabel("Volume [m³]")
        plt.title("Relação entre Xa e Volume")

        # Ajuste de curva
        z = np.polyfit(Xa, V, 1)
        p = np.poly1d(z)
        plt.plot(Xa, p(Xa), label='Curva de ajuste', color='red')

        # Exibir a equação da reta no gráfico
        equacao_label = f"Equação: V = {z[0]:.2f}Xa"
        plt.text(0.1, 0.8, equacao_label, transform=plt.gca().transAxes)

        plt.legend()
        plt.grid(True)
        plt.show()
    except ValueError:
        resposta_label["text"] = "Erro ao gerar o gráfico. Verifique as entradas."


def jan_CSTR():

    #Janela principal
    main2 = Toplevel(main)
    main2.focus_set()
    main2.resizable(False,False)
    Label(main2, text="Cálculo de volume de um reator CSTR [m³]").grid(column=0, row=0)

    #Fluxo molar de A
    texto_Fa_ra = Label(main2, text="Forneça a relação de Fa/(-ra) [m³]")
    texto_Fa_ra.grid(column=0, row=1, padx=50, pady=10)
    global Fa_ra_entry
    Fa_ra_entry = Entry(main2, bd=2)
    Fa_ra_entry.grid(column=0, row=2, padx=50, pady=10)
    Fa_ra_entry.focus_set()

    #Fração de A que reagiu
    texto_Xa = Label(main2, text="Forneça a fração de A que reagiu")
    texto_Xa.grid(column=0, row=3, padx=50, pady=10)
    global Xa_entry
    Xa_entry = Entry(main2, bd=2)
    Xa_entry.grid(column=0, row=4, padx=50, pady=10)

    botao_resultado = Button(main2, text="Calcular o Volume [m³]", command=CSTR, state=DISABLED)
    botao_resultado.grid(column=0, row=5, padx=50, pady=10)

    global resposta_label
    resposta_label = Label(main2, text="")
    resposta_label.grid(column=0, row=6)

    # Botão para gerar o gráfico
    global botao_grafico
    botao_grafico = Button(main2, text="Gerar Gráfico", command=graf_CSTR, state=DISABLED)
    botao_grafico.grid(column=0, row=9, padx=10, pady=10)

    # Verificar campos de entrada para habilitar botão do gráfico
    def verificar_campos(*args):
        if Xa_entry.get() and Fa_ra_entry.get():
            botao_resultado["state"] = NORMAL
        else:
            botao_resultado["state"] = DISABLED

    Xa_entry.bind("<KeyRelease>", verificar_campos)
    Fa_ra_entry.bind("<KeyRelease>", verificar_campos)

    # Sair da janela
    Button(main2, text="Sair", command=lambda: [main2.destroy(), main.deiconify(), EQ2.config(state=NORMAL)]) \
        .grid(column=0, row=10, padx=50, pady=10)
    main2.protocol("WM_DELETE_WINDOW", lambda: [main2.destroy(), main.deiconify(), EQ2.config(state=NORMAL)])


#Cálculo de volume PFR, onde V = Fai.{integral [dXa/(-ra)]}

#Reação A -> 2B, portanto -ra = kCa

#V = (Qi/k).ln (1/1-xa)

def PFR():

    Qi = Qi_entry.get()
    xa = Xa_entry.get()
    k = K_entry.get()
    try:
        Qi = float(Qi.replace(",","."))
        try:
            xa = float(xa.replace(",","."))
            if xa > 1 or xa <= 0:
                raise RuntimeError
            else:
                try:
                    k = float(k.replace(",","."))
                    try:
                        V = (Qi/k)*np.log(1/(1-xa))
                        V = round(V,2)
                        if V > 0:
                            resposta_label["text"] = f"O volume necessário é de {V} L."

                            botao_grafico["state"] = NORMAL
                        else:
                            resposta_label["text"] = "As entradas deverão ser maiores que 0."
                    except ValueError:
                        resposta_label["text"] = "Favor insira apenas números"
                except ValueError:
                    resposta_label["text"] = "Favor insira apenas números"
                except RuntimeError:
                    resposta_label["text"] = "Xa deve ser maior que 0 e menor que 1."
        except RuntimeError:
            resposta_label["text"] = "Xa deve ser maior que 0 e menor que 1."
        except ValueError:
            resposta_label["text"] = "Favor insira apenas números"
    except ValueError:
        resposta_label["text"] = "Favor insira apenas números"

def graf_PFR():
    try:
        Qi = Qi_entry.get()
        Qi = float(Qi.replace(",", "."))
        k = K_entry.get()
        k = float(k.replace(",", "."))
        xa = np.linspace(0.01, 0.99, 100)
        V = (Qi / k) * np.log(1 / (1 - xa))

        # Criar o gráfico
        plt.plot(xa, V, label="Curva")
        plt.title('Relação entre Xa e Volume')
        plt.xlabel('Xa')
        plt.ylabel('Volume [m³]')
        plt.grid(True)
        plt.legend()

        # Exibir a equação da curva no gráfico
        equacao_label = f"Equação: V = ({Qi:.2f}/{k:.2f}) * ln(1 / (1 - Xa))"
        plt.text(0.05, 0.85, equacao_label, transform=plt.gca().transAxes)

        # Exibir o gráfico
        plt.show()

    except ValueError:
        resposta_label["text"] = "Erro ao gerar o gráfico. Verifique as entradas."

def jan_PFR():

    #Janela principal
    main2 = Toplevel(main)
    main2.focus_set()
    main2.resizable(False,False)
    Label(main2, text="Cálculo de volume de um reator PFR [L]").grid(column=0, row=0)

    #Vazão de A
    texto_Qi = Label(main2, text="Forneça a Vazão de alimentação de A [L/s]")
    texto_Qi.grid(column=0, row=1, padx=50, pady=10)
    global Qi_entry
    Qi_entry = Entry(main2, bd=2)
    Qi_entry.grid(column=0, row=2, padx=50, pady=10)
    Qi_entry.focus_set()

    #Constante de reação de A
    texto_K = Label(main2, text="Forneça a velocidade de reação de A [1/s]")
    texto_K.grid(column=0, row=3, padx=50, pady=10)
    global K_entry
    K_entry = Entry(main2, bd=2)
    K_entry.grid(column=0, row=4, padx=50, pady=10)

    #Fração de A que reagiu
    texto_Xa = Label(main2, text="Forneça a fração de A que reagiu")
    texto_Xa.grid(column=0, row=5, padx=50, pady=10)
    global Xa_entry
    Xa_entry = Entry(main2, bd=2)
    Xa_entry.grid(column=0, row=6, padx=50, pady=10)

    botao_resultado = Button(main2, text="Calcular o Volume [L]", command=PFR, state=DISABLED)
    botao_resultado.grid(column=0, row=7, padx=50, pady=10)

    global resposta_label
    resposta_label = Label(main2, text="")
    resposta_label.grid(column=0, row=8)

    # Botão para gerar o gráfico
    global botao_grafico
    botao_grafico = Button(main2, text="Gerar Gráfico", command=graf_PFR, state=DISABLED)
    botao_grafico.grid(column=0, row=9, padx=10, pady=10)

    # Verificar campos de entrada para habilitar botão do gráfico
    def verificar_campos(*args):
        if Xa_entry.get() and Qi_entry.get() and K_entry.get():
            botao_resultado["state"] = NORMAL
        else:
            botao_resultado["state"] = DISABLED

    Xa_entry.bind("<KeyRelease>", verificar_campos)
    Qi_entry.bind("<KeyRelease>", verificar_campos)
    K_entry.bind("<KeyRelease>",verificar_campos())

    # Sair da janela
    Button(main2, text="Sair", command=lambda: [main2.destroy(), main.deiconify(), EQ3.config(state=NORMAL)]) \
        .grid(column=0, row=10, padx=50, pady=10)
    main2.protocol("WM_DELETE_WINDOW", lambda: [main2.destroy(), main.deiconify(), EQ3.config(state=NORMAL)])


main = Tk()

main.title("Cálculo Cinética Aplicada à Reatores")
main.resizable(False, False)
main.geometry("400x200")

# Impedir de criar várias janelas
EQ1 = Button(main, text="A+B->C+D BR", command=lambda:[jan_BR(),EQ1.config(state=DISABLED)])
EQ1.place(relx=0.5, rely=0.25, anchor=CENTER)

EQ2 = Button(main, text="Volume CSTR", command=lambda:[jan_CSTR(),EQ2.config(state=DISABLED)])
EQ2.place(relx=0.5, rely=0.5, anchor=CENTER)

EQ3 = Button(main, text="Volume PFR", command=lambda:[jan_PFR(),EQ3.config(state=DISABLED)])
EQ3.place(relx=0.5, rely= 0.75, anchor=CENTER)

Button(main, text="Sair", command=lambda:[main.destroy,fechar_graf()]).place(relx=0.025, rely=0.95, anchor=SW)
main.protocol("WM_DELETE_WINDOW", lambda: [main.destroy,fechar_graf()])

main.mainloop()

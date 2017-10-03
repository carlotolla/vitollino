#! /usr/bin/env python
# -*- coding: UTF8 -*-
# Este arquivo é parte do programa Vittolino
# Copyright 2011-2017 Carlo Oliveira <carlo@nce.ufrj.br>,
# `Labase <http://labase.selfip.org/>`__, `GPL <http://is.gd/3Udt>`__.
#
# Vittolino é um software livre, você pode redistribuí-lo e/ou
# modificá-lo dentro dos termos da Licença Pública Geral GNU como
# publicada pela Fundação do Software Livre (FSF), na versão 2 da
# Licença.
#
# Este programa é distribuído na esperança de que possa ser útil,
# mas SEM NENHUMA GARANTIA, sem uma garantia implícita de ADEQUAÇÃO
# a qualquer MERCADO ou APLICAÇÃO EM PARTICULAR. Veja a
# Licença Pública Geral GNU para maiores detalhes.
#
# Você deve ter recebido uma cópia da Licença Pública Geral GNU
# junto com este programa, se não, veja em <http://www.gnu.org/licenses/>
"""
Gerador de labirintos e jogos tipo 'novel'.
"""
from browser import document, html

SZ = dict(W=300, H=300)
DOC_PYDIV = document["pydiv"]
ppcss = 'https://codepen.io/imprakash/pen/GgNMXO'
STYLE = {'position': "absolute", 'width': SZ['W'], 'left': 0, 'top': 0}
PSTYLE = {'position': "absolute", 'width': SZ['W'], 'left': 0, 'bottom': 0}
LIMBOSTYLE = {'position': "absolute", 'width': SZ['W'], 'left': 10000, 'bottom': 0, 'background': "white"}
ISTYLE = {'opacity': "inherited", 'height': 30, 'left': 0, 'top': 0, 'background': "white"}
ESTYLE = {'opacity': "inherited", 'width': 30, 'height': 30, 'min-height': '30px', 'float': 'left', 'position': 'unset'}
EIMGSTY = {"max-width": "100%", "max-height": "100%"}
STYLE["min-height"] = "300px"
IMAGEM = ""
NSTYLE = {'position': "absolute", 'width': "60%", 'left': "20%", 'top': 0, 'margin': "0%",
          "min-height": "20%", "cursor": "n-resize"}
SSTYLE = {'position': "absolute", 'width': "60%", 'left': "20%", 'bottom': 0, 'margin': "0%",
          "min-height": "10%", "cursor": "s-resize"}
LSTYLE = {'position': "absolute", 'width': "10%", 'left': "90%", 'top': "20%", 'margin': "0%",
          "min-height": "60%", "cursor": "e-resize"}
OSTYLE = {'position': "absolute", 'width': "10%", 'left': 0, 'top': "20%", 'margin': "0%",
          "min-height": "60%", "cursor": "w-resize"}
ZSTYLE = {'position': "absolute", 'width': "10%", 'margin': "0%",
          "min-height": "10%", "cursor": "zoom-in"}
# INVENTARIO = None


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


@singleton
class SalaCenaNula:
    def __init__(self):
        self.esquerda, self.direita = [None] * 2
        self.salas = [None] * 5
        self.cenas = [self] * 4
        self.img = "_NO_IMG_"
        self.nome = "_NO_NAME_"
        self.init = self.init
        self.centro, self.norte, self.leste, self.sul, self.oeste = self.salas

    def init(self):
        self.init = lambda _=0, s=self: self
        self.esquerda, self.direita = [SalaCenaNula()] * 2
        self.salas = [SalaCenaNula()] * 5
        self.cenas = [SalaCenaNula()] * 4
        self.centro, self.norte, self.leste, self.sul, self.oeste = self.salas
        return self

    def vai(self):
        pass

    def portal(self, *_, **__):
        pass


NADA = SalaCenaNula().init()
NS = {}
NL = []


class Musica(object):
    def __init__(self, sound, loop=True, autoplay=True, sound_type="audio/mpeg"):
        self.sound = html.AUDIO(src=sound, autoplay=autoplay, loop=loop, type=sound_type)
        document.body <= self.sound


class Elemento:
    """
    Um objeto de interação que é representado por uma imagem em uma cena.

            papel = Elemento(
             img="papel.png", tit="caderno de notas",
             vai=pega_papel, style=dict(left=350, top=550, width=60))


    :param img: URL de uma imagem
    :param vai: função executada quando se clica no objeto
    :param style: dicionário com dimensões do objeto {"left": ..., "top": ..., width: ..., height: ...}
    :param tit: Texto que aparece quando se passa o mouse sobre o objeto
    :param alt: Texto para leitores de tela
    :param tel: cena alternativa onde o objeto vai ser colocado
    :param kwargs: lista de parametros nome=URL que geram elementos com este nome e a dada imagem
    """
    limbo = html.DIV(style=LSTYLE)

    def __init__(self, img="", vai=None, style=NS, tit="", alt="", tel=DOC_PYDIV, **kwargs):
        self.img = img
        self.vai = vai if vai else lambda _=0: None
        self.tela = tel
        self.opacity = 0
        self.style = dict(**PSTYLE)
        # self.style["min-width"], self.style["min-height"] = w, h
        self.style.update(style)
        self.elt = html.DIV(Id=tit, style=self.style)
        if img:
            self.img = html.IMG(src=img, title=tit, alt=alt, style=EIMGSTY)  # width=self.style["width"])
            self.elt <= self.img
        self.elt.onclick = self._click
        self.tela <= self.elt
        self.c(**kwargs)

    def _click(self, _=None):
        return self.vai()

    def entra(self, cena, style=None):
        self.elt.style = style if style else self.style
        cena <= self

    @classmethod
    def c(cls, **kwarg):
        return [setattr(cls, nome, Elemento(img) if isinstance(img, str) else img) for nome, img in kwarg.items()]


class Portal:
    N = NSTYLE
    L = LSTYLE
    S = SSTYLE
    O = OSTYLE
    Z = ZSTYLE
    PORTAIS = dict(N=NSTYLE, L=LSTYLE, S=SSTYLE, O=OSTYLE, Z=ZSTYLE)

    def __init__(self, cena=None, **kwargs):
        self.kwargs = kwargs
        self.style = ZSTYLE
        if cena:
            self.cena = cena
            self.p(**kwargs)

    def __call__(self, cena):
        class CenaDecorada(cena):
            def __init__(self, *args, __portal=self, **kargs):
                style = ZSTYLE
                super(CenaDecorada, self).__init__(*args, **kargs)
                __portal.cena = self
                [__portal.__setup__(acena, portal, style) for portal, acena in __portal.kwargs.items()]

        return CenaDecorada

    def __setup__(self, cena, portal, style=NS):
        class Portico:
            def __init__(self, origem, destino, portal_, style_):
                self.origem, self.destino, self.portal_, self.style_ = origem, destino, portal_, style_
                self.elt = html.DIV(style=self.style_)
                self.elt.onclick = lambda *_: self.vai()
                Droppable(self.elt, cursor="not-allowed")
                if isinstance(self.origem, Cena):
                    self.origem.elt <= self.elt
                    setattr(self.origem, portal, self)
                self.vai = self.vai
                self._vai = self.vai

            def __call__(self, *args, **kwargs):
                return self.vai(*args)

            def fecha(self, *_):
                self.vai = lambda *_: None

            def abre(self, *_):
                self.vai = self._vai

            def vai(self, *_):
                return self.destino.vai()

            @property
            def img(self):
                return self.destino.img

            def __eq__(self, other):
                return other == self.destino
        _ = style.update({"min-height": style["height"]}) if "height" in style else None
        sty = Portal.PORTAIS.get(portal, ZSTYLE)
        self.style.update(sty)
        self.style.update(style)
        ptc = Portico(self.cena, cena, portal, self.style)
        self.elt = ptc.elt
        return self.cena

    def p(self, style=NS, **kwargs):
        [self.__setup__(cena, portal, style) for portal, cena in kwargs.items() if cena != NADA]
        return self.cena


ROSA = list("NLSO")
CART = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # [(i, j) for j, i in CART]


class Labirinto:
    def __init__(self, c=NADA, n=NADA, l=NADA, s=NADA, o=NADA):
        self.salas = [sala for sala in [c, n, l, s, o]]
        self.centro, self.norte, self.leste, self.sul, self.oeste = self.salas
        for indice, sala in enumerate(self.salas[1:]):
            self.centro.cenas[indice].portal(N=sala.cenas[indice])
            indice_oposto = (indice + 2) % 4
            sala.cenas[indice_oposto].portal(N=self.centro.cenas[indice_oposto])

    @staticmethod
    def m(cenas):
        def valid(cns, jj, ii, m, n):
            return 0 <= jj + m < len(cns) and 0 <= ii + n < len(cns[jj + m]) and cns[jj + m][ii + n]

        def vizinhos(jj, ii, cns=cenas):
            return [(kk, cns[jj + m][ii + n]) for kk, (m, n) in enumerate(CART) if valid(cns, jj, ii, m, n)]
            # return [(kk, cns[jj + m][ii + n]) for kk, (m, n) in enumerate(CART)
            #  if 0 <= jj + m < len(cns) and 0 <= ii + n < len(cns[jj+m])and cns[jj + m][ii + n]]

        for j, linha in enumerate(cenas):
            if isinstance(linha, list):
                for i, centro in enumerate(linha):
                    if not isinstance(centro, Sala):
                        continue
                    for k, sala in vizinhos(j, i):
                        if not isinstance(sala, Sala):
                            continue
                        centro.cenas[k].portal(**{"N": sala.cenas[k]})
                        indice_oposto = (k + 2) % 4
                        sala.cenas[indice_oposto].portal(**{"N": centro.cenas[indice_oposto]})


class Sala:
    def __init__(self, n=NADA, l=NADA, s=NADA, o=NADA, nome='', **kwargs):
        self.cenas = [Cena(img) if isinstance(img, str) else img for img in [n, l, s, o]]
        self.nome = nome
        Sala.c(**kwargs)
        self.p()

    @property
    def norte(self):
        return self.cenas[0]

    @property
    def leste(self):
        return self.cenas[1]

    @property
    def sul(self):
        return self.cenas[2]

    @property
    def oeste(self):
        return self.cenas[3]

    def p(self):
        for esquerda in range(4):
            cena_a_direita = (esquerda + 1) % 4
            self.cenas[esquerda].direita = self.cenas[cena_a_direita]
            self.cenas[cena_a_direita].esquerda = self.cenas[esquerda]

    @staticmethod
    def c(**cenas):
        for nome, cena in cenas.items():
            setattr(Sala, nome, Sala(*cena, nome=nome))


class Salao(Sala):
    def p(self):
        # [cena.sai(saida) for cena, saida in zip(self.cenas, saidasnlso)]
        for esquerda in range(4):
            cena_a_direita = (esquerda + 1) % 4
            self.cenas[esquerda].portal(L=self.cenas[cena_a_direita])
            self.cenas[cena_a_direita].portal(O=self.cenas[esquerda])

    @staticmethod
    def c(**cenas):
        for nome, cena in cenas.items():
            setattr(Salao, nome, Salao(*cena, nome=nome))


class Cena:
    """
    Use para construir uma cena.
    ::

        from _spy.vitollino import Cena

        cena_esq = Cena(img="esq.jpg")
        cena_mei = Cena(img="mei.jpg", cena_esq)
        cena_mei.vai()

    :param str img: URL da imagem
    :param Cena esquerda: Cena que está à esquerda desta
    :param Cena direita: Cena que está à direita desta
    :param Cena meio: Cena que está à frente desta
    :param vai: Função a ser chamada no lugar da self.vai nativa
    """

    def __init__(self, img=IMAGEM, esquerda=NADA, direita=NADA, meio=NADA, vai=None, nome='', **kwargs):
        width = STYLE["width"]
        self.img = img
        self.nome = nome
        self.dentro = []
        self.esquerda, self.direita, self.meio = esquerda or NADA, direita or NADA, meio or NADA
        self.N, self.O, self.L = [NADA] * 3
        self.vai = vai or self.vai
        self.elt = html.DIV(style=STYLE)
        self.elt <= html.IMG(src=self.img, width=width, style=STYLE, title=nome)
        Cena.c(**kwargs)

        self._cria_divs(width)

    def _cria_divs(self, width):
        self.divesq = divesq = html.DIV(style=STYLE)
        divesq.style.opacity = 0
        divesq.style.width = width // 3  # 100
        Droppable(divesq, cursor="not-allowed")
        divesq.onclick = self.vai_esquerda
        self.divmeio = divmeio = html.DIV(style=STYLE)
        divmeio.style.opacity = 0
        divmeio.style.width = width // 3  # 100
        divmeio.onclick = self.vai_meio
        Droppable(divmeio, cursor="not-allowed")
        divmeio.style.left = width // 3  # 100
        self.divdir = divdir = html.DIV(style=STYLE)
        divdir.style.opacity = 0
        divdir.style.width = width // 3  # 100
        divdir.onclick = self.vai_direita
        Droppable(divdir, cursor="not-allowed")
        divdir.style.left = width * 2 // 3  # 100
        self.elt <= self.divesq
        self.elt <= self.divmeio
        self.elt <= self.divdir

    def __call__(self):
        return self.vai()

    def __le__(self, other):
        if hasattr(other, 'elt'):
            self.elt <= other.elt
        else:
            self.elt <= other
            print(other)

    def portal(self, esquerda=None, direita=None, meio=None, **kwargs):
        self.esquerda, self.direita, self.meio = esquerda or self.esquerda, direita or self.direita, meio or self.meio
        return Portal(self, **kwargs)

    @staticmethod
    def c(**cenas):
        for nome, imagem in cenas.items():
            setattr(Cena, nome, Cena(imagem, nome=nome))

    @staticmethod
    def q(n=NADA, l=NADA, s=NADA, o=NADA, nome="", **kwargs):
        return Sala(n, l, s, o, nome=nome, **kwargs)

    @staticmethod
    def s(n=NADA, l=NADA, s=NADA, o=NADA, nome="", **kwargs):
        return Salao(n, l, s, o, nome=nome, **kwargs)

    def vai_direita(self, _=0):
        if self.direita:
            self.direita.vai()

    def vai_esquerda(self, _=0):
        if self.esquerda:
            self.esquerda.vai()

    def vai_meio(self, _=0):
        if self.meio:
            self.meio.vai()

    def sai(self, saida):
        self.meio = saida

    def bota(self, item):
        self.dentro.append(item)
        self <= item

    def tira(self, item):
        self.dentro.pop(item)

    def vai(self):
        INVENTARIO.cena = self
        INVENTARIO.desmonta()
        tela = DOC_PYDIV
        tela.html = ""
        tela <= self.elt
        INVENTARIO.monta()
        INVENTARIO.cena = self
        return self


class Popup:
    POP = None

    def __init__(self, cena, tit="", txt="", vai=None, **kwargs):
        self.cena, self.tit, self.txt, = cena, tit, txt
        self.kwargs = kwargs
        self._vai = vai
        Popup.__setup__()
        if isinstance(cena, Cena):
            self.d(cena, tit, txt)

    def vai(self):
        return self._vai() if self._vai else None

    def __call__(self, cena=None, tit="", txt="", *args, **kwargs):
        cena = cena or self.cena
        out = cena(*args, **kwargs)
        self.d(out, tit or self.tit, txt or self.txt)

        return out  # CenaPopup

    @staticmethod
    def __setup__():
        class Pop:
            def __init__(self, tela=DOC_PYDIV):
                self.tela = tela
                self.popup = html.DIV(Id="__popup__", Class="overlay")
                div = html.DIV(Class="popup")
                self.tit = html.H2()
                a = html.A("&times;", Class="close", href="#")
                self.go = html.A(Id="txt_button", Class="button", href="#__popup__")
                self.go.onclick = self._open
                a.onclick = self._close
                self.alt = html.DIV(Class="content")
                self.popup <= div
                self.popup.style = {"visibility": "hidden", "opacity": 0}
                div <= self.tit
                div <= a
                div <= self.alt

            def _close(self, *_):
                self.popup.style = {"visibility": "hidden", "opacity": 0}

            def _open(self, *_):
                self.popup.style = {"visibility": "visible", "opacity": 0.7}

            def mostra(self, act, tit="", txt=""):
                if tit or txt:
                    self.tit.text, self.alt.text = tit, txt
                # self.popup.style = {"visibility": "visible", "opacity": 0.7}
                self._open()
                act()

        Popup.POP = Pop()
        Popup.__setup__ = lambda: None

    @staticmethod
    def d(cena, tit="", txt=""):
        cena.elt <= Popup.POP.popup
        cena.elt <= Popup.POP.go
        act = cena.vai
        cena.vai = lambda _=0: Popup.POP.mostra(act, tit, txt)
        return cena


class Texto(Popup):
    def __init__(self, cena=NADA, tit="", txt="", **kwargs):
        self.elt = Popup.POP.popup
        cena <= self
        super().__init__(None, tit=tit, txt=txt, vai=None, **kwargs)

    def vai(self):
        print("Texto(Popup)", self.tit, self.txt)
        Popup.POP.mostra(lambda *_: None, self.tit, self.txt)
        pass


@singleton
class Inventario:
    def __init__(self, tela=DOC_PYDIV):
        self.tela = tela
        self.cena = None
        self.inventario = {}
        self.opacity = 0
        self.style = dict(**ISTYLE)
        self.style["min-height"] = "30px"
        self.elt = html.DIV(Id="__inv__", style=self.style)
        self.elt.onclick = self.mostra
        self.limbo = html.DIV(style=self.style)
        self.limbo.style.left = "4000px"
        self.mostra()
        tela <= self.elt

    def __le__(self, other):
        if hasattr(other, 'elt'):
            self.elt <= other.elt
        else:
            self.elt <= other

    def inicia(self):
        self.elt.html = ""
        self.cena = None
        self.opacity = 0
        self.mostra()

    def desmonta(self, _=0):
        self.limbo <= self.elt

    def monta(self, _=0):
        self.tela <= self.elt

    def mostra(self, _=0):
        self.opacity = abs(self.opacity - 0.5)
        self.elt.style.opacity = self.opacity

    def bota(self, nome_item, item="", acao=None):
        if isinstance(nome_item, str):
            item_img = html.IMG(Id=nome_item, src=item, width=30, style=EIMGSTY)
            self.elt <= item_img
        else:
            nome_item.entra(self)
            item_img = nome_item.elt
            item_img.style = ESTYLE
        Dropper(item_img)
        if acao:
            item_img.onclick = lambda *_: acao()
        else:
            acao = lambda *_: None
        self.inventario[nome_item] = acao

    def tira(self, nome_item):
        item_img = document[nome_item]
        self.inventario.pop(nome_item, None)
        self.limbo <= item_img


INVENTARIO = Inventario()


class Dropper:
    def __init__(self, dropper):
        dropper.draggable = True
        dropper.ondragstart = self.drag_start
        dropper.onmouseover = self.mouse_over

    def mouse_over(self, ev):
        ev.target.style.cursor = "pointer"

    def drag_start(self, ev):
        ev.data['text'] = ev.target.id
        ev.data.effectAllowed = 'move'
        ev.preventDefault()
        return False


class Droppable:
    def __init__(self, droppable, dropper_name="", action=None, cursor=None):
        # droppable.ondragover = self.drag_over
        # droppable.ondrop = self.drop
        droppable.bind("dragover", self.drag_over)
        droppable.bind("drop", self.drop)
        self.dropper_name = dropper_name
        self.cursor = cursor
        self.action = action if action else lambda *arg: None

    def drag_over(self, ev):
        ev.data.dropEffect = 'move'
        # print('drop', ev.target.id)
        src_id = ev.data['text']
        elt = document[src_id]
        elt.style.cursor = self.cursor or "auto"
        ev.preventDefault()

    def drop(self, ev):
        ev.preventDefault()
        src_id = ev.data['text']
        elt = document[src_id]
        elt.style.cursor = "auto"
        if self.dropper_name == src_id:
            self.action(elt, self)


class Folha:
    def __init__(self, texto, ht_ml, tela, left):
        style = {'position': "absolute", 'width': 80, 'height': 80, 'left': left, 'top': 10, 'background': "yellow"}
        fid = "folha%d" % left
        self.folha = ht_ml.DIV(texto, Id=fid, style=style, draggable=True)
        tela <= self.folha
        self.folha.ondragstart = self.drag_start
        self.folha.onmouseover = self.mouse_over

    def mouse_over(self, ev):
        ev.target.style.cursor = "pointer"

    def drag_start(self, ev):
        ev.data['text'] = ev.target.id
        ev.data.effectAllowed = 'move'


class Suporte:
    def __init__(self, bloco, ht_ml, tela, left, certa):
        style = {'position': "absolute", 'width': 80, 'height': 80, 'left': left, 'top': 100, 'background': "grey"}
        self.folha = ht_ml.DIV("............ ............", style=style)
        self.left = left
        self.certa = certa
        tela <= self.folha
        self.folha.ondragover = self.drag_over
        self.folha.ondrop = self.drop
        self.bloco = bloco

    def drag_over(self, ev):
        ev.data.dropEffect = 'move'
        ev.preventDefault()

    def drop(self, ev):
        ev.preventDefault()
        src_id = ev.data['text']
        elt = document[src_id]
        elt.style.left = self.left
        elt.style.top = 100
        elt.draggable = False  # don't drag any more
        elt.style.cursor = "auto"
        certa = True
        if src_id != self.certa:
            elt.style.background = "red"
            certa = False
            self.bloco.conta_peça(certa)


class Bloco:
    def __init__(self):
        self.monta = lambda *_: None
        ordem = "10 410 310 210 110".split()
        texto = "" \
                "Era uma vez|" \
                "de nós três|" \
                "por cima|" \
                "deu um salto|" \
                "um gato pedrêz|" \
                "".split("|")
        tela = document["pydiv"]
        tela.html = ""
        self.pecas_colocadas = []
        print(list(enumerate(ordem)))
        for pos, fl in enumerate(ordem):
            Suporte(self, html, tela, pos * 100 + 10, "folha" + fl)
        for pos, tx in enumerate(texto):
            Folha(tx, html, tela, pos * 100 + 10)

    def inicia_de_novo(self):
        pass

    def conta_pecas(self, valor_peca):
        self.pecas_colocadas += valor_peca
        if len(self.pecas_colocadas) == 4:
            if all(self.pecas_colocadas):
                input("O texto está certo.")
            else:
                vai = input("Tentar de novo?")
                if vai == "s":
                    self.inicia_de_novo()

    def nao_monta(self):
        pass

    def vai(self):
        self.monta()
        self.monta = self.nao_monta
        # self.centro.norte.vai()


class Jogo:
    def __init__(self):
        self.cena = self.c = Cena
        self.quarto = self.q = Sala
        self.salao = self.s = Salao
        self.algo = self.a = Elemento
        self.texto = self.t = Popup
        self.labirinto = self.l = Labirinto
        self.inventario = self.i = INVENTARIO
        self.portal = self.p = Portal
        self.dropper = self.d = Dropper
        self.droppable = self.r = Droppable
        self.musica = self.m = Musica
        pass


JOGO = Jogo()


def main():
    # Bloco()
    # CenaPrincipal()
    return Bloco()


if "__main__" in __name__:
    main()

CSS = '''
h1 {
  text-align: center;
  font-family: Tahoma, Arial, sans-serif;
  color: #06D85F;
  margin: 80px 0;
}

.box {
  width: 40%;
  margin: 0 auto;
  background: rgba(255,255,255,0.2);
  padding: 35px;
  border: 2px solid #fff;
  border-radius: 20px/50px;
  background-clip: padding-box;
  text-align: center;
}

.button {
  position: absolute;
  font-size: 1em;
  padding: 10px;
  color: #fff;
  border: 2px solid #FFF3;
  border-radius: 100px;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.3s ease-out;
  left: 45%;
  top: 25%;
}
.button:hover {
  background: #777;
}

.overlay {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.7);
  transition: opacity 300ms;
}
.overlay:target {
  visibility: visible;
  opacity: 0.8;
}

.popup {
  top: 20%;
  margin: 70px auto;
  padding: 15px;
  background: #fff;
  border-radius: 10px;
  width: 85%;
  position: relative;
  transition: all 5s ease-in-out;
}

.popup h2 {
  margin-top: 0;
  color: #333;
  font-family: Tahoma, Arial, sans-serif;
}
.popup .close {
  position: absolute;
  top: 0px;
  right: 5px;
  transition: all 200ms;
  font-size: 30px;
  font-weight: bold;
  text-decoration: none;
  color: #333;
}
.popup .close:hover {
  color: #06D85F;
}
.popup .content {
  max-height: 30%;
  overflow: auto;
}
'''


def __setup__():
    document.head <= html.STYLE(CSS, type="text/css", media="screen")
    Popup(Cena())


__setup__()

#tarzan/main.py
#vader/main.py
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
Gerador de labirintos e jogos tipo 'novel
https://github.com/carlotolla/vitollino
"""
from _spy.vitollino.vitollino import STYLE, INVENTARIO, Cena
from _spy.vitollino.vitollino import JOGO
Cena._cria_divs = lambda *_: None
STYLE['width'] = 800
STYLE['min-height'] = "800px"
INVENTARIO.elt.style.width = 800
ACTIV = "https://activufrj.nce.ufrj.br/file/GamesInteligentesII/Cena_1_Quadro_{}_Momento_{}.jpg"
QUADROS = [list(range(1,3)),list(range(1,9)),[1]]
MOMENTOS = [(quadro+1, momento)
        for quadro, quadros in enumerate(QUADROS) for momento in quadros]

LEGENDAS = "vestiário abriu_o_armário o_asseio acionou_a_pia molhando_as_mãos usando_sabão" \
           " as_bactérias enxaguando secando descontaminando saindo".split()
CONFIGURA = dict(
    origem=\
    ["vestiário#vestiário#Asseio#Você deve por o avental", True,dict(left=429, top=112, width=109, height=300)],
    vestiário=\
    ["vestiário#abriu_o_armário#Asseio#Você deve por o avental", True,dict(left=429, top=112, width=109, height=300)],
    abriu_o_armário=\
    ["abriu_o_armário#o_asseio#Asseio#Você deve lavar as mão", True,dict(left=429, top=112, width=109, height=300)],
    o_asseio=\
    ["o_asseio#acionou_a_pia#o_asseio#acionou_a_pia", True,dict(left=354, top=653, width=60, height=60)],
    acionou_a_pia=\
    ["acionou_a_pia#molhando_as_mãos#o_asseio#acionou_a_pia", True,dict(left=354, top=653, width=60, height=60)],
    molhando_as_mãos=\
    ["molhando_as_mãos#usando_sabão#o_asseio#acionou_a_pia", True,dict(left=429, top=112, width=109, height=300)],
    usando_sabão=\
    ["usando_sabão#as_bactérias#o_asseio#acionou_a_pia", True,dict(left=429, top=112, width=109, height=300)],
    as_bactérias=\
    ["as_bactérias#enxaguando#o_asseio#acionou_a_pia", True,dict(left=429, top=112, width=109, height=300)],
    enxaguando=\
    ["enxaguando#secando#o_asseio#acionou_a_pia", True,dict(left=429, top=112, width=109, height=300)],
    secando=\
    ["secando#descontaminando#o_asseio#acionou_a_pia", True,dict(left=429, top=112, width=109, height=300)],
    descontaminando=\
    ["descontaminando#saindo#o_asseio#acionou_a_pia", True,dict(left=429, top=112, width=109, height=300)],
)

class JogoMarcela:
    def __init__(self, legendas=LEGENDAS, momentos=MOMENTOS):
        """
        Constroi o jogo completo da Marcela.

        :param legendas: lista contendo nomes das cenas *[<nome da cena>, ...]*
        :param momentos: lista de tuplas indicando o quadro e o momento  *[(<q0>, <m0>), ... ]*
        """
        self.quadros = momentos
        telas = {nome: ACTIV.format(quadro, momento) for nome, (quadro, momento) in zip(legendas, momentos)}
        print({te: ur[-18:] for te, ur in telas.items()})
        self.cenario = self._cria_cenas(telas)
        self._inicia_jogo()

    def _configura_momentos(self, cena):
        origem_destino_titulo_texto, com_texto, hot = CONFIGURA[cena]
        origem, destino, titulo, texto = origem_destino_titulo_texto.split("#")
        origem = getattr(JOGO.c, origem)
        jogo = self

        class PreviaDoMomento:
            def __init__(self):
                self.destino = destino
                self._destino = getattr(JOGO.c, destino)
                self.nome = self._destino.nome

            def vai(self, *_, **__):
                jogo._configura_momentos(self.destino)
                self._destino.vai(*_, **__)


        @JOGO.n.texto(titulo, texto)
        def configura_portal_com_texto(origem_, destino_, hot_spot=hot):
            return origem_.portal(L=destino_, style=hot_spot)

        def configura_portal_sem_texto(origem_, destino_, hot_spot=hot):
            return origem_.portal(L=destino_, style=hot_spot)

        previo_destino = PreviaDoMomento()

        if com_texto:
            configura_portal_com_texto(origem, previo_destino)
        else:
            configura_portal_sem_texto(origem, previo_destino)


        return previo_destino

    def _inicia_jogo(self):
        self._configura_momentos("origem").vai()

    @staticmethod
    def _cria_cenas(cenas):
        """
        Cria um conjunto de objetos **Cena** a partir de um dicionário.

        Usa a função cria cenas do Vitollino: *JOGO.c.c*

        :param cenas:dicionário contendo *<nome da cena>: <url da imagem>*
        :return: cenário, uma lista de quadros criados
        """
        JOGO.c.c(**cenas)
        return []  # [self._cria_cena(quadro+1, self.quadros[quadro]) for quadro in range(0,3)]


def main(*_):
    JogoMarcela()
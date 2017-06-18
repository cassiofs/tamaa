#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import re
import itertools

from unicodedata import normalize
import unicodedata

# py -3 -m pip install pandas
import pandas as pd
from pandas import DataFrame

# py -3 -m pip install nltk
# py -m nltk.downloader all
from nltk.corpus import stopwords

from nltk.stem import SnowballStemmer

def preprocessamento(txt):
	texto = txt

    #remove acentos
	texto = normalize('NFKD', texto).encode('ASCII','ignore').decode('ASCII').lower()

    #remove url
	texto = re.sub(r"http\S+", "", texto)

	#remove hashtag
	texto = re.sub(r"#\S+", "", texto)

	#remove rt
	if texto[:3] == 'rt ':
		texto = texto[3:]

	#remove a string 'mchef' para normalizar os nomes dos participantes
	texto = texto.replace('mchef','')

	#remove stopwords
	texto =  ' '.join([word for word in texto.split() if word not in (stopwords.words('portuguese'))])

	#remove acentos e caracteres especiais
	nfkd = unicodedata.normalize('NFKD', texto) # Unicode normalize transforma um caracter em seu equivalente em latin.
	palavraSemAcento = u"".join([c for c in nfkd if not unicodedata.combining(c)])
	texto = re.sub('[^a-zA-Z0-9 \\\]', '', palavraSemAcento) # Usa expressão regular para retornar a palavra apenas com números, letras e espaço

    # retira caracteres duplicados
	texto = ''.join(ch for ch, _ in itertools.groupby(texto))

    # estemizar
	#texto = stemmer.stem(texto)

    # retira espaços no início e final do texto
	texto = texto.strip()

	return texto


stemmer = SnowballStemmer("portuguese")

# cria arquivo de saída
arquivoarff = open('resultado.arff','w')
# escreve cabeçalho do WEKA no arquivo
arquivoarff.write('@relation resultado'+'\n')
arquivoarff.write('\n')
#arquivoarff.write('@attribute user string'+'\n')
arquivoarff.write('@attribute tweet string'+'\n')
arquivoarff.write('@attribute relevante {S,N}'+'\n')
arquivoarff.write('\n')
arquivoarff.write('@data'+'\n')
arquivoarff.write('\n')

df = pd.read_csv('corpus-1.tsv', sep='\t', encoding='utf-8')
df.columns = ['id','user','text','created_at','rel1','rel2','rel','concorda']
for i, linha in df.iterrows():  #i: índice do dataframe index; linha: cada linha no formato série
	linhax = preprocessamento(linha['text'])
	# trata a composição da classe: 'relevante'
	relfinal = 'N'
	if linha['rel1'] == 'S' and linha['rel2'] == 'S':
		relfinal = "S"
	#relfinal = linha['rel2']
	# grava a linha no arquivo, no formato WEKA
	arquivoarff.write( '\'' + linhax + '\',' + relfinal + '\n')

df = pd.read_csv('corpus-2.tsv', sep='\t', encoding='utf-8')
df.columns = ['id','user','text','created_at','rel1','rel2','rel','concorda']
for i, linha in df.iterrows():  #i: índice do dataframe index; linha: cada linha no formato série
	linhax = preprocessamento(linha['text'])
	# trata a composição da classe: 'relevante'
	relfinal = 'N'
	if linha['rel1'] == 'S' and linha['rel2'] == 'S':
		relfinal = "S"
	#relfinal = linha['rel2']
	# grava a linha no arquivo, no formato WEKA
	arquivoarff.write( '\'' + linhax + '\',' + relfinal + '\n')

df = pd.read_csv('corpus-3.tsv', sep='\t', encoding='utf-8')
df.columns = ['id','user','text','created_at','rel1','rel2','rel','concorda']
for i, linha in df.iterrows():  #i: índice do dataframe index; linha: cada linha no formato série
	linhax = preprocessamento(linha['text'])
	# trata a composição da classe: 'relevante'
	relfinal = 'N'
	if linha['rel1'] == 'S' and linha['rel2'] == 'S':
		relfinal = "S"
	#relfinal = linha['rel2']
	# grava a linha no arquivo, no formato WEKA
	arquivoarff.write( '\'' + linhax + '\',' + relfinal + '\n')

arquivoarff.close()

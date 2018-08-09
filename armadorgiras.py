# -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 12:00:20 2018

@author: sduran

SUGERENCIA: AGREGAR CORRECCION DE ERRORES. DAR LA LISTA AL FINAL DE CADA 
PROGRAMA Y PREGUNTAR SI HAY QUE CAMBIAR ALGO.
"""
import sys
import xlsxwriter
from itertools import permutations

def mala_gira(gira,equipos):
    malagira = True
    while malagira:
            if gira:
                malagira = False
            for equipo in gira.split():
                if equipo.upper() not in equipos:
                    malagira = True
                    print '%s no es un equipo válido.' % (equipo)
            if malagira:
                gira = raw_input('Volvé a ingresar la gira: ')
    return gira

def mala_gira2(gira_base,permuta,equipos,autovisita):
    malagira = True
    while malagira:
            malagira = False
                
            for equipo in gira_base:
                if equipo.upper() not in equipos:
                    malagira = True
                    print '%s no es un equipo válido.' % (equipo)
                if equipo.upper()==autovisita.upper():
                    malagira = True
                    print '%s no se puede visitar a sí mismo.' % (equipo)
            if malagira:
                gira_base = raw_input("Tu opción de permuta es '%s', pero la gira está mal ingresada. "
                "Volvé a ingresar *solo* la gira separada por espacios, o tocá enter: " % (permuta) )
                gira_base = gira_base.upper().split()
    return gira_base

def fijo_primero(gira_base):
    fijo = gira_base.pop(0)
    aux = list(permutations(gira_base))
    gyp = []
    for gira in aux:
        a = list(gira)
        a.insert(0,fijo)
        gyp.append(a)
    for gira in aux:
        b = list(gira)
        b.append(fijo)
        gyp.append(b)
    return gyp
    
def fijo_medio(gira_base):
    saco1 = gira_base.pop(0)
    saco2 = gira_base.pop(-1)
    aux = list(permutations(gira_base))
    gyp = [] 
    for gira in aux:
        a = list(gira)
        a.insert(0,saco1) 
        a.append(saco2)
        gyp.append(a)
        b = list(gira)
        b.insert(0,saco2)
        b.append(saco1)
        gyp.append(b)
    return gyp
    
def asigno_permutaciones(gira_base,permuta):
    posibles_respuestas = ['t','n','fm','fp']
    while (permuta not in posibles_respuestas) or (permuta == 'fm' and len(gira_base)<3) or (permuta == 'fp' and len(gira_base)<3):
        permuta = raw_input('No es una respuesta válida para permutar. Poné otra: ')
    if permuta == 't':
        gyp = list(permutations(gira_base))
        
    elif permuta == 'n':
        gyp = [gira_base]
        
    elif permuta == 'fp':
        gyp = fijo_primero(gira_base)
    
    elif permuta == 'fm':
        gyp = fijo_medio(gira_base)
    return { 'gyp' : gyp, 'permuta' : permuta }

def archivo(giras):
    workbook = xlsxwriter.Workbook('./giras.xlsx')
    worksheet = workbook.add_worksheet('Giras')
    row = 0
    for equipo in giras.keys():
        for gira in giras[equipo]:
            col = 0
            worksheet.write(row,col,row+1)
            worksheet.write(row,col+1, equipo)
            worksheet.write(row,col+2, len(gira))
            col = 3
            for element in gira:
                worksheet.write(row,col,str(element))
                col += 1
            for i in range(col,7):
                worksheet.write(row,i,'xxx')
            row += 1
    return
    
    

def equipos():
    nro_equipos = input('¿Cuántos equipos juegan? ')
    equipos = []
    print 'Poné las siglas de 3 letras de cada equipo. Es indistinto si es minúscula o mayúscula.'
    for i in range(nro_equipos):
        
        equipos.append(raw_input( "%d) " % (i+1) ).upper())
        #equipos[i].upper()
        while  (len(equipos[i]) != 3) or (equipos[i].isalpha() == False):
            equipos[i] = (raw_input('Te dije 3 letras papá. De vuelta. %d) ' % (i+1) ).upper())
    return equipos



#ACA EMPIEZAN LOS PROGRAMAS POSTA

    
def giras_comunes(equipos):
    print '''Acá introducís las giras que se van a repetir, aclarando si se usa con permutaciones.
        Pensá en usar nombres cortos para las giras. Cuando no tengas más giras para agregar, tocá enter.
        Las que no se incluyan acá se pueden agregar a mano individualmente para cada equipo. '''
    giras_comunes = {}
    recordatorio_giras= {}
    
    nombre_gira = raw_input('¿Cómo llamamos a la gira? ')
    
    no_mas_giras = nombre_gira == ''
     
    
    while not no_mas_giras:
        #nombres_giras.append(raw_input('¿Cómo llamamos a la gira? '))
              
        gira = raw_input('Poné los equipos de la gira separados por espacios: ')
        
        gira = mala_gira(gira,equipos)        
              
        gira_base = gira.upper().split()
        gira_base2 = gira.upper().split()
        
        permuta = raw_input('''¿Usamos permutaciones? Código: <n>: no, <t>: todas las permutaciones. Si son al menos 3 equipos, 
            <fm> : fijo el del medio, <fp>: se empieza o termina en el primero ingresado. ''')

        result = asigno_permutaciones(gira_base2,permuta)
        gyp = result['gyp']
        permuta = result['permuta']
            
        #IDEA: chequear que en un set de "giras y permutaciones" no haya giras repetidas.
        
                        
        giras_comunes[nombre_gira.title()]=gyp
        
        
        recordatorio_giras[nombre_gira.title()] = [gira_base, permuta, '%d giras.' %(len(gyp))]
        #recordatorio_giras[nombre_gira].append(len(gyp))
        #recordatorio_giras[nombre_gira] = [recordatorio_giras[nombre_gira],len(gyp)]
        
        nombre_gira = raw_input('Si querés agregar una gira, poné el nombre. Sino, tocá enter. ')
        if nombre_gira in recordatorio_giras.keys():
            nombre_gira = raw_input('Ese nombre ya está usado, poné otro, o tocá enter para terminar. ')
        no_mas_giras = nombre_gira == ''
    
    #IDEA: que te permita chequear giras, cambiar o eliminar.    
    
    print 'Esta es la lista de giras que queda.'            
    
    for key in sorted(recordatorio_giras.keys()):
        print key, ' ', recordatorio_giras[key]    
    
    
    f = open('giras_comunes.txt','w')
    print 'hello'
    s = str(recordatorio_giras)    
    f.write(s)
    f.close()
    
    return recordatorio_giras, giras_comunes
    
#giras_comunes(equipos())
#giras_comunes(['MAM','LAL','ASA','TUV'])


def giras():
    
    #IDEA: preguntar si se quiere retomar un excel o empezar de cero
    #IDEA: preguntar el nombre del fixture para que sea el nombre del archivo
    #IDEA: integrar de alguna manera el programa de arriba de las giras comunes,
        #sea armando un set en este programa, o sea armando un archivo en ese programa
        #y después tomándolo en este.
    
    giras = {}
    
    listaequipos = equipos()
    
    equipo = raw_input('¿Por qué equipo empezamos? ')
    equipo = equipo.upper()
    while equipo not in listaequipos:
        equipo = raw_input('%s no es un equipo válido, volvé a ingresarlo. ' % (equipo))
        equipo = equipo.upper()
    
    while equipo:    
        giras[equipo] = []
        gira = raw_input("Ingresá su primera gira, separada por espacios. Si querés agregar permutaciones, "
            "agregá al princpio: <t>: todas las permutaciones. Si son al menos 3 equipos, <fm> : fijo el "
            "del medio, <fp>: se empieza o termina en el primero ingresado. ")
        
        while gira:
            
            while len(gira.split()[0]) < 3 and len(gira.split())==1:
                gira = raw_input('Mal ingresado. Volve a poner la gira: ')            
            
            if len(gira.split()[0]) >= 3 :
                gira_base = gira.upper().split()
                gira = 'n ' + gira
            
            else:
                gira_base = gira.upper().split()
                gira_base.pop(0)
            
            permuta = gira.split()[0]                                                        
            gira_base = mala_gira2(gira_base,permuta,listaequipos,equipo)
            
            if gira_base:            
                result = asigno_permutaciones(gira_base,permuta)
                gyp = result['gyp']
                permuta = result['permuta']
                
        
                for gira in gyp:
                    if list(gira) not in giras[equipo]:
                        giras[equipo].append(list(gira))
                    else:
                        print '[%s] ya estaba entre las giras, no la agregamos.' % (', '.join(gira))
            else:
                print 'La gira quedó vacía, no agregamos nada.'
            
            gira = raw_input("Ingresá otra gira, separada por espacios. Si ya terminaste con "
            "las giras de este equipo, tocá enter. ")
        
        equipo = raw_input('¿Por qué equipo seguimos? Si ya terminaste, tocá enter. ')
        while equipo.upper() not in listaequipos and equipo:
            equipo = raw_input('%s no es un equipo válido, volvé a ingresarlo.' % (equipo))

                
        equipo = equipo.upper()
        
        #IDEA: chequear que un equipo visita todos los otros equipos
        #IDEA: chequear que todos los equipos tengan sus giras
    
    archivo(giras)
    
    print 'Te queda esto: '
    print giras
           
    return giras
    



def main():
    print '''Bienvenido al armador de giras. Estoy hecho para ahorrarte tiempo 
        al armar el excel de las giras para cualquier fixture. Así que si no te ahorro tiempo,
        ya sabés, no me uses.'''
    
    #nombre_fixture = raw_input('¿Qué fixture tenés que hacer? ')
    
if __name__ == '__main__':
    giras()

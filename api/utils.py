#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string
import random


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    """
    Función para generar valores aleatorios
    Puede recibir:
        size = longitud de la cadena
            Defecto 6
        chars = caracteres a utilizar para buscar la cadena
            Defecto letras mayusculas y numeros
    """
    return ''.join(random.choice(chars) for _ in range(size))
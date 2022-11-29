import random

class Hormiga:
  def __init__(self,n_obj, capacidad):
    self.solucion = []
    self.valor = 0
    self.capacidad = capacidad
    self.peso = 0
    self.n_obj = n_obj
  
  def reestablecer_datos(self, capacidad):
    self.solucion = [0 for i in range(self.n_obj)]
    self.valor = 0
    self.capacidad = capacidad
    self.peso = 0

  def crear_solucion(self, valores, pesos, feromonas, heuristicas, alfa, beta):
    objetos_disponibles = [i for i in range(self.n_obj)]
    # Se agrega un objeto a la mochila aleatoriamente
    r = random.randint(0, self.n_obj-1) # Se elige un numero de 0 a Numero de objetos - 1
    self.solucion[r] = 1 # Se agrega a la solucion
    self.valor += valores[r]
    self.peso += pesos[r]
    self.capacidad -= pesos[r]
    # Se quita de los objetos disponibles
    objetos_disponibles.remove(r)
    while not es_vacio(objetos_disponibles):
      # Calcular los productos Tao_j * Mu_j
      productos = calcular_productos(feromonas, heuristicas, objetos_disponibles, alfa, beta)
      suma = sum(productos)
      probabilidades = calcular_probabilidades(productos, suma)

      # Elegir el objeto para agregarlo a la mochila
      indice_obj = elegir_objeto(probabilidades, objetos_disponibles) 
      self.solucion[indice_obj] = 1

      # Actualizar valores
      self.capacidad -= pesos[indice_obj]
      self.peso += pesos[indice_obj]
      self.valor += valores[indice_obj]

      # Quitamos el objeto de disponibles
      objetos_disponibles.remove( indice_obj )

      # Actualizamos los objetos disponibles de la mochila
      actualizacion_objetos_disponibles(objetos_disponibles, pesos, self.capacidad)


  def __obtener_valores_solucion(self, valores):
    valores_solucion = []
    for i in range(self.n_obj):
      if self.solucion[i] == 1:
        valores_solucion.append( valores[i] )

    return valores_solucion

  def depositar_feromonas(self, valores, feromonas):
    z_best = max( self.__obtener_valores_solucion(valores) )
    for i in range(self.n_obj):
      if self.solucion[i] == 1:
        feromonas[i] += 1 / (1 + (z_best - valores[i]/ z_best))
  
  def obtener_valores(self, valores):
    val = 0
    for i in range(self.n_obj):
      if self.solucion[i] == 1:
        val += valores[i]
    return val

  def obtener_pesos(self, pesos):
    val = 0
    for i in range(self.n_obj):
      if self.solucion[i] == 1:
        val += pesos[i]
    return val
  
  def __str__(self):
    return f'Solucion = {self.solucion} Valor = {self.valor}, Peso = {self.peso}'


def calcular_heuristicas(valores, pesos, n):
  heuristicas = []
  for i in range(n):
    heuristica = valores[i] / (pesos[i]**2)
    heuristicas.append( heuristica )

  return heuristicas

def es_vacio(objetos_disponibles):
  return len(objetos_disponibles) == 0

def calcular_productos(feromonas, heuristicas , disponibles, alfa, beta):
  productos = []
  for i in range(len(disponibles)):
    j = disponibles[i]
    p = (feromonas[j]**alfa)* (heuristicas[j]**beta)
    productos.append(p)

  return productos

def calcular_probabilidades(productos, suma):
  if suma == 0: return []
  probabilidades = []
  for producto in productos:
    probabilidad = producto / suma
    probabilidades.append(probabilidad)
  
  return probabilidades

def elegir_objeto(probabilidades, disponibles):
  if es_vacio(probabilidades):
    return random.choice(disponibles) # Devuelve un numero aleatorio de los objetos disponibles
  probabilidad_mejor = probabilidades[0]
  mejor = disponibles[0]
  for i in range(1,len(disponibles)):
    if probabilidad_mejor < probabilidades[i]:
      probabilidad_mejor = probabilidades[i]
      mejor = disponibles[i]
  # Regresa el valor de la lista de objeto de disponibles
  return mejor

def actualizacion_objetos_disponibles(disponibles, pesos, capacidad):
  # print('Disponibles = ', disponibles)
  # print('Pesos = ', pesos)
  n = len(disponibles)
  i = 0
  while i < n:
    if pesos[disponibles[i]] > capacidad:
      disponibles.pop(i)
      n -= 1
    else: i += 1

def evaporar_feromonas(feromonas, ro, n_obj):
  for i in range(n_obj):
    feromonas[i] = feromonas[i]*(1-ro)

def agregar_feromonas(hormigas, feromonas, valores):
  for hormiga in hormigas:
      hormiga.depositar_feromonas(valores, feromonas)

def mejor_hormiga(hormigas, num_hormigas):
  mejor_hormiga = hormigas[0]
  for i in range(1, num_hormigas):
    if mejor_hormiga.valor < hormigas[i].valor:
      mejor_hormiga = hormigas[i]
  
  return mejor_hormiga



def aco_mochila(valores, pesos, capacidad_total, n_obj, n_hormigas):
  # Inicializar parametros
  alfa = 1
  beta = 5
  ro = 0.5
  heuristicas = calcular_heuristicas(valores, pesos, n_obj)
  feromonas = [0 for i in range(n_obj)]
  MAX = 10
  iteracion = 0
  # Crear hormigas
  hormigas = []
  for i in range(n_hormigas):
    hormigas.append( Hormiga(n_obj, capacidad_total) )

  while iteracion < MAX:
    print('iteracion: ', iteracion)
    for hormiga in hormigas:
      hormiga.reestablecer_datos(capacidad_total)
      # print(hormiga)
    print('Construyendo soluciones')
    print('Valores')
    print(valores)
    print('Pesos')
    print(pesos)
    for hormiga in hormigas:
      hormiga.crear_solucion(valores, pesos, feromonas, heuristicas, alfa, beta)
      print(hormiga)
      # print('Valor = ', hormiga.obtener_valores(valores))
      # print('Peso = ', hormiga.obtener_pesos(pesos))
    
    # Evaporar feromonas 
    evaporar_feromonas(feromonas, ro, n_obj)

    # Agregar feromonas
    agregar_feromonas(hormigas, feromonas, valores)
    print(feromonas)
    iteracion += 1
  
  return mejor_hormiga(hormigas, n_hormigas)


def main():
  # Inicializando parametros
  num_h = 10
  n_objetos = 10
  valor_maximo = 30
  peso_maximo = 50
  capacidad_total = 100
  valores = [random.randint(1, valor_maximo) for i in range(n_objetos)]
  pesos = [random.randint(1, peso_maximo) for i in range(n_objetos)]
  hormiga = aco_mochila(valores, pesos, capacidad_total, n_objetos, num_h)
  print('Capacidad = ', capacidad_total)
  print('Valores = ', valores)
  print('Pesos = ', pesos)
  print(f'Mejor Hormiga: Solucion = {hormiga.solucion}, Valor = {hormiga.valor}, Peso = {hormiga.peso}')
  


if __name__ == '__main__':
  main()
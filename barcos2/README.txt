Batalla Naval en Docker (Servidor-Cliente)
Descripción
batalla Naval, pelea de barcos o como gusten llamar es un juego PvP donde se tienen que atacar por turnos los jugadores ahora 
diremos las caracteristicas del juego:

El tablero es de 4x4, representado con caracteres ASCII.
~ representa el mar.
@ representa la posición del cursor para apuntar.
* marca los disparos realizados.

Cada jugador tiene un barco de 3 casillas.
Los jugadores se conectan al servidor para:
Colocar su barco.

Alternar turnos para apuntar y disparar.

El primer jugador en hundir el barco del oponente gana.

El servidor coordina los turnos, valida los movimientos y muestra el estado del tablero actualizado a cada cliente.
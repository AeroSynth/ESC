EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Connector:AudioJack3 J?
U 1 1 64853FB1
P 5550 3225
F 0 "J?" H 5270 3250 50  0001 R CNN
F 1 "AudioJack-Lavalier" H 5270 3204 50  0000 R CNN
F 2 "" H 5550 3225 50  0001 C CNN
F 3 "~" H 5550 3225 50  0001 C CNN
	1    5550 3225
	-1   0    0    -1  
$EndComp
$Comp
L Connector:AudioPlug3 J?
U 1 1 6485494D
P 3700 3225
F 0 "J?" H 3757 3592 50  0001 C CNN
F 1 "AudioPlug" H 3757 3500 50  0000 C CNN
F 2 "" H 3800 3175 50  0001 C CNN
F 3 "~" H 3800 3175 50  0001 C CNN
	1    3700 3225
	1    0    0    -1  
$EndComp
$Comp
L Device:CP C?
U 1 1 64854F1B
P 4800 3225
F 0 "C?" V 4545 3225 50  0001 C CNN
F 1 "1uF" V 4637 3225 50  0000 C CNN
F 2 "" H 4838 3075 50  0001 C CNN
F 3 "~" H 4800 3225 50  0001 C CNN
	1    4800 3225
	0    1    1    0   
$EndComp
$Comp
L Device:R R?
U 1 1 64855670
P 4525 3325
F 0 "R?" V 4318 3325 50  0001 C CNN
F 1 "2.2K" V 4525 3325 50  0000 C CNN
F 2 "" V 4455 3325 50  0001 C CNN
F 3 "~" H 4525 3325 50  0001 C CNN
	1    4525 3325
	0    1    1    0   
$EndComp
Wire Wire Line
	5350 3125 5225 3125
Wire Wire Line
	4650 3225 4300 3225
Wire Wire Line
	5350 3225 5225 3225
Wire Wire Line
	5225 3225 5225 3125
Connection ~ 5225 3125
Wire Wire Line
	5225 3125 4300 3125
Wire Wire Line
	4950 3225 5050 3225
Wire Wire Line
	5050 3225 5050 3325
Wire Wire Line
	5050 3325 5350 3325
Wire Wire Line
	4675 3325 5050 3325
Connection ~ 5050 3325
Wire Wire Line
	4375 3325 4300 3325
$EndSCHEMATC

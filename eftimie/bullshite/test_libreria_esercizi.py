from eftimie import libreria_esercizi
import pytest

def test_E1_Triangoli_classifier():
    assert libreria_esercizi.E1_Triangoli_classifier([7, 7, 10]) == 'ISOSCELE'
    assert libreria_esercizi.E1_Triangoli_classifier([10, 10, 100]) == 'N/A'
    assert libreria_esercizi.E1_Triangoli_classifier([7, 2, 10]) == 'N/A'
    assert libreria_esercizi.E1_Triangoli_classifier([15, 7, 10]) == 'SCALENO'
    assert libreria_esercizi.E1_Triangoli_classifier([7, 7, 10]) == 'ISOSCELE'
    assert libreria_esercizi.E1_Triangoli_classifier([7, 7, 7]) == 'EQUILATERO'

def test_E1_Triangoli_area():
    assert libreria_esercizi.E1_Triangoli_area([7, 7, 10]) == 24.49
    # TODO assert su presenza di 'math domain error'
    with pytest.raises(ValueError, match=r"Il triangolo non è valido, perimetro non calcolabile"):
        libreria_esercizi.E1_Triangoli_area([10, 10, 100])
    with pytest.raises(ValueError, match=r"Il triangolo non è valido, perimetro non calcolabile"):
        libreria_esercizi.E1_Triangoli_area([7, 2, 10])
    assert libreria_esercizi.E1_Triangoli_area([15, 7, 10]) == 29.39
    assert libreria_esercizi.E1_Triangoli_area([7, 7, 10]) == 24.49
    assert libreria_esercizi.E1_Triangoli_area([7, 7, 7]) == 21.22

def test_E1_Triangoli_perimetro():
    assert libreria_esercizi.E1_Triangoli_perimetro([7, 7, 10]) == 24
    with pytest.raises(ValueError, match=r"Il triangolo non è valido, perimetro non calcolabile"):
        libreria_esercizi.E1_Triangoli_area([10, 10, 100])
    with pytest.raises(ValueError, match=r"Il triangolo non è valido, perimetro non calcolabile"):
        libreria_esercizi.E1_Triangoli_perimetro([7, 2, 10])
    assert libreria_esercizi.E1_Triangoli_perimetro([15, 7, 10]) == 32
    assert libreria_esercizi.E1_Triangoli_perimetro([7, 7, 10]) == 24
    assert libreria_esercizi.E1_Triangoli_perimetro([7, 7, 7]) == 21

def test_E1_Triangoli_isValidTriangolo():
    assert libreria_esercizi.E1_Triangoli_isValidTriangolo(7, 7, 10) == True
    assert libreria_esercizi.E1_Triangoli_isValidTriangolo(10, 10, 100) == False
    assert libreria_esercizi.E1_Triangoli_isValidTriangolo(7, 2, 10) == False
    assert libreria_esercizi.E1_Triangoli_isValidTriangolo(15, 7, 10) == True

def test_E3_ListaStringa():
    assert libreria_esercizi.E3_ListaStringa(["Mario", "Luigi", "PrincipessaPeach", "Bowser", "Toad"]) == "Mario_Luigi_PrincipessaPeach_Bowser_Toad"
    assert libreria_esercizi.E3_ListaStringa([]) == ""
    assert libreria_esercizi.E3_ListaStringa(["Mario"]) == "Mario"
    assert libreria_esercizi.E3_ListaStringa([" "]) == " "
    assert libreria_esercizi.E3_ListaStringa([" ", "Mario"]) == " _Mario"
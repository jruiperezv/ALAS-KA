'''
Created on 26/04/2013

@author: jruiperezv
'''

class Subject:
    def __init__(self, code, name):
        self.code = code
        self.name = name
        
class MeasureBlock:
    def __init__(self, code, name):
        self.code = code
        self.name = name
        
class Exercise:
    def __init__(self, code, name):
        self.id = code
        self.name = name
         
class Video:
    def __init__(self, code, youtube_id):
        self.id = code
        self.youtube_id = youtube_id
               
class Utils:
    @staticmethod
    def getSubjectList():
        return [Subject(1, 'Physics'), Subject(2, 'Chemistry'), Subject(3, 'Mathematics')]
    
    @staticmethod
    def getMeasureList():
        return [MeasureBlock(1, 'Total Use of the Platform'), MeasureBlock(2, 'Correct Progress on the Platform'), 
                MeasureBlock(3, 'Time Distribution of Use of the Platform'), MeasureBlock(4, 'Gamification Habits'),
                MeasureBlock(5, 'Exercise Solving Habits'),MeasureBlock(6, 'Course Evaluation')]
     
    @staticmethod   
    def getExerciseList():
        return[Exercise(26003,'d_ejercicio_corriente_electrica'), Exercise(22007,'d_ejercicio_voltaje'), 
               Exercise(13006,'d_ejercicio_ley_de_ohm'), Exercise(22008,'d_ejercicio_de_magnetismo'), 
               Exercise(21005,'d_ejercicio_fuerza_de_lorentz'), Exercise(20004,'d_ejercicio_radio_de_Larmor'), 
               Exercise(14003,'d_ejercicio_ley_de_faraday_1'), Exercise(22009,'d_ejercicio_ley_de_faraday_2'), 
               Exercise(23006,'d_ejercicio_ley_de_faraday_3'), Exercise(16003,'d_ejercicio_producto_escalar'),
               Exercise(15006,'d_ejercicio_movimiento_armonico_simple'), Exercise(15007,'d_ejercicio_ondas_armonicas_1a'), 
               Exercise(21003,'d_ejercicio_ondas_armonicas_1b'), Exercise(23004,'d_ejercicio_ondas_armonicas_1c'), 
               Exercise(22006,'d_ejercicio_ondas_armonicas_2a'), Exercise(23005,'d_ejercicio_ondas_armonicas_2c'), 
               Exercise(16005,'d_ejercicio_ondas_armonicas_2d'), Exercise(13004,'d_ejercicio_ondas_armonicas_2b'), 
               Exercise(19002,'d_ejercicio_carga_electrica'), Exercise(13005,'d_ejercicio_principio_de_superposicion'),
               Exercise(21004,'d_ejercicio_ley_de_gauss_1'), Exercise(19003,'d_ejercicio_ley_de_gauss_2'),
               Exercise(17005,'d_ejercicio_ley_de_gauss_3'),Exercise(25002,'d_ejercicio_sistemas_unidades'),
               Exercise(16004,'d_ejercicio_producto_vectorial'), Exercise(23002,'d_ejercicio_escalares_y_vectores'), 
               Exercise(15003,'d_ejercicio_tiro_parabolico'), Exercise(20002,'d_ejercicio_movimiento_circular'), 
               Exercise(24002,'d_ejercicio_fuerza_rozamiento'), Exercise(23003,'d_ejercicio_plano_inclinado_a'), 
               Exercise(15004,'d_ejercicio_plano_inclinado_b'), Exercise(22004,'d_ejercicio_fuerza_centripeta'),
               Exercise(15005,'d_ejercicio_trabajo_y_energia_2'), Exercise(17004,'d_ejercicio_trabajo_y_energia_3'),
               Exercise(22005,'d_ejercicio_trabajo_y_energia_1')]
        
    @staticmethod
    def getVideoList():
        return[Video(25001,'QnFAinppDuY'),Video(22003,'1qN6iYXFq4M'),
               Video(17003,'5xb2fQMk6uM'),Video(15002,'NJxmQQH4Ino'),
               Video(26001,'99_1evO9LIo'),Video(26002,'fLYGVPaXQZY'),
               Video(14002,'ESSg3pdsSqA'),Video(15001,'EJ37y9lmXcM'),
               Video(22001,'_bQuu6ZcQWM'),Video(17002,'WKR3h7vBxtU'),
               Video(22002,'EQ4JVdRLxlU'),Video(23001,'q1SM0TwBVB8'),
               Video(24001,'ED2m8ha0YtE'),Video(21002,'NwZqpCAf6o8'),
               Video(14001,'5XXjcYatNSc'),Video(20036,'Y2ROdOQX6eo'),
               Video(13001,'48Ql6brAFo4'),Video(16001,'xl8LDsCpji0'),
               Video(13002,'NCXidrDO2Kw'),Video(13003,'PgyDMfHgZ50'),
               Video(18001,'jkR4yELP9dM'),Video(19001,'7jj6zSWEEgk'),
               Video(20001,'eOrER1YVZO4'),Video(18002,'Kowq757A9n4'),
               Video(21001,'ybNT-irAr_w'),Video(16002,'UYDUUEtR6so')]
        
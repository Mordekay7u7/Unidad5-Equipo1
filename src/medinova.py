from datetime import datetime


class CitaDuplicadaError(Exception):
    pass

class CanalWhatsAppBloqueadoError(Exception):
    pass

class LimiteSobrecupoAlcanzadoError(Exception):
    pass

class MedicoNoAceptaSobrecupoError(Exception):
    pass

class Paciente:
    def __init__(self, nombre: str, inasistencias_previas: int = 0):
        self.nombre = nombre
        self.inasistencias_previas = inasistencias_previas

class Medico:
    def __init__(self, nombre: str, permite_sobrecupo: bool = False):
        self.nombre = nombre
        self.permite_sobrecupo = permite_sobrecupo
        self.sobrecupos_actuales: int = 0

class SistemaGestionCitas:
    def __init__(self):
        self.citas_registradas = []

    def agendar_cita(self, paciente: Paciente, fecha_hora: datetime, canal: str = "PRESENCIAL", pago_anticipado: bool = False):
        if paciente.inasistencias_previas >= 3 and canal in ["WHATSAPP", "TELEFONO"] and not pago_anticipado:
            print(f"\n  [RECHAZADO] Acción: Agendamiento Bloqueado | Razón: Paciente {paciente.nombre} acumula {paciente.inasistencias_previas} no-shows en 6 meses (Canal {canal} no permitido)")
            raise CanalWhatsAppBloqueadoError("Agendamiento digital bloqueado")

        for cita in self.citas_registradas:
            if cita["paciente"] == paciente.nombre and cita["fecha_hora"] == fecha_hora:
                print(f"\n  [RECHAZADO] Acción: Cita Duplicada Bloqueada | Razón: El paciente {paciente.nombre} ya tiene cita activa a las {fecha_hora.strftime('%H:%M')}")
                raise CitaDuplicadaError("Cita duplicada a la misma hora")

        nueva_cita = {
            "paciente": paciente.nombre,
            "fecha_hora": fecha_hora,
            "estado": "CONFIRMADA",
            "canal": canal
        }
        self.citas_registradas.append(nueva_cita)
        
        razon = "Horario Libre" if canal != "PRESENCIAL" or not pago_anticipado else "Pago por adelantado en recepción (Excepción por no-shows)"
        print(f"\n  [ÉXITO] Acción: Cita Agendada | Razón: {razon} | Paciente: {paciente.nombre} | Canal: {canal}")
        return nueva_cita

    def agendar_sobrecupo(self, medico: Medico, paciente: Paciente):
        if not medico.permite_sobrecupo:
            print(f"\n  [RECHAZADO] Acción: Sobrecupo Denegado | Razón: El Dr(a). {medico.nombre} NO tiene habilitada la opción de sobrecupo en su perfil")
            raise MedicoNoAceptaSobrecupoError("Médico no acepta sobrecupo")
        
        if medico.sobrecupos_actuales >= 2:
            print(f"\n  [RECHAZADO] Acción: Sobrecupo Denegado | Razón: El Dr(a). {medico.nombre} ya alcanzó el límite máximo de 2 sobrecupos en el turno")
            raise LimiteSobrecupoAlcanzadoError("Límite de sobrecupos alcanzado")
        
        medico.sobrecupos_actuales += 1
        print(f"\n  [ÉXITO] Acción: Sobrecupo Asignado | Razón: Autorizado por médico ({medico.sobrecupos_actuales}/2 asignados) | Paciente: {paciente.nombre} | Médico: {medico.nombre}")
        return f"Sobrecupo asignado a {paciente.nombre}"
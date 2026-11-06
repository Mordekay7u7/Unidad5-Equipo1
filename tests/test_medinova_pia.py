from datetime import UTC, datetime, timedelta

import pytest

# --- Clases de Dominio Simuladas de MediNova ---

class DuplicateAppointmentError(Exception):
    pass

class ChannelBlockedError(Exception):
    pass

class OverbookingLimitExceeded(Exception):
    pass

class OverbookingNotAllowed(Exception):
    pass

class Patient:
    def __init__(self, patient_id: int, no_shows_count: int = 0):
        self.patient_id = patient_id
        self.no_shows_count = no_shows_count

class Doctor:
    def __init__(self, doctor_id: int, allows_overbooking: bool = False):
        self.doctor_id = doctor_id
        self.allows_overbooking = allows_overbooking
        self.current_overbookings: int = 0

class AppointmentService:
    def __init__(self):
        self.appointments = []

    def schedule_appointment(self, patient: Patient, date_time: datetime, channel: str = "PRESENTIAL", paid_upfront: bool = False):
        # Regla 2: No-shows recurrentes (3 o más bloquean canal digital)
        if patient.no_shows_count >= 3 and channel in ["WHATSAPP", "PHONE"] and not paid_upfront:
            raise ChannelBlockedError("Agendamiento digital bloqueado por no-shows recurrentes")

        # Regla 1: Prevenir citas duplicadas
        for app in self.appointments:
            if app["patient_id"] == patient.patient_id and app["date_time"] == date_time and app["status"] != "CANCELLED":
                raise DuplicateAppointmentError("El paciente ya tiene una cita en este horario")

        appointment = {"patient_id": patient.patient_id, "date_time": date_time, "status": "RESERVED", "channel": channel}
        self.appointments.append(appointment)
        return appointment

    def schedule_overbooking(self, doctor: Doctor, patient: Patient, date_time: datetime):
        # Regla 3: Sobrecupo según médico
        if not doctor.allows_overbooking:
            raise OverbookingNotAllowed("El médico no acepta sobrecupo")
        if doctor.current_overbookings >= 2:
            raise OverbookingLimitExceeded("Límite máximo de 2 sobrecupos alcanzado por turno")
        
        doctor.current_overbookings += 1
        return {"doctor_id": doctor.doctor_id, "patient_id": patient.patient_id, "type": "OVERBOOKING"}

# --- Pruebas Automáticas Pytest (9 Casos del PIA) ---

now = datetime.now(UTC)

# --- Regla 1: Citas Duplicadas ---
def test_cp01_schedule_success():
    service = AppointmentService()
    p1 = Patient(1)
    app = service.schedule_appointment(p1, now)
    assert app["status"] == "RESERVED"

def test_cp02_schedule_duplicate_error():
    service = AppointmentService()
    p1 = Patient(1)
    service.schedule_appointment(p1, now)
    with pytest.raises(DuplicateAppointmentError):
        service.schedule_appointment(p1, now)

def test_cp03_schedule_same_day_different_hour():
    service = AppointmentService()
    p1 = Patient(1)
    service.schedule_appointment(p1, now)
    later = now + timedelta(hours=1)
    app2 = service.schedule_appointment(p1, later)
    assert app2["status"] == "RESERVED"

# --- Regla 2: No-shows ---
def test_cp04_noshow_under_limit_whatsapp():
    service = AppointmentService()
    p2 = Patient(2, no_shows_count=1)
    app = service.schedule_appointment(p2, now, channel="WHATSAPP")
    assert app["channel"] == "WHATSAPP"

def test_cp05_noshow_limit_reached_whatsapp_blocked():
    service = AppointmentService()
    p3 = Patient(3, no_shows_count=3)
    with pytest.raises(ChannelBlockedError):
        service.schedule_appointment(p3, now, channel="WHATSAPP")

def test_cp06_noshow_limit_presential_with_payment():
    service = AppointmentService()
    p3 = Patient(3, no_shows_count=3)
    app = service.schedule_appointment(p3, now, channel="PRESENTIAL", paid_upfront=True)
    assert app["status"] == "RESERVED"

# --- Regla 3: Sobrecupo ---
def test_cp07_overbooking_success():
    service = AppointmentService()
    dr_garza = Doctor(101, allows_overbooking=True)
    p = Patient(4)
    res = service.schedule_overbooking(dr_garza, p, now)
    assert res["type"] == "OVERBOOKING"

def test_cp08_overbooking_limit_exceeded():
    service = AppointmentService()
    dr_garza = Doctor(101, allows_overbooking=True)
    dr_garza.current_overbookings = 2
    p = Patient(5)
    with pytest.raises(OverbookingLimitExceeded):
        service.schedule_overbooking(dr_garza, p, now)

def test_cp09_overbooking_not_allowed():
    service = AppointmentService()
    dr_trevino = Doctor(102, allows_overbooking=False)
    p = Patient(6)
    with pytest.raises(OverbookingNotAllowed):
        service.schedule_overbooking(dr_trevino, p, now)
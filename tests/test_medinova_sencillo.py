from datetime import datetime, timedelta, timezone
import pytest

# IMPORTACIÓN CLAVE: Ahora los tests llamarán directamente a src/medinova.py
from src.medinova import (
    SistemaGestionCitas,
    Paciente,
    Medico,
    CitaDuplicadaError,
    CanalWhatsAppBloqueadoError,
    LimiteSobrecupoAlcanzadoError,
    MedicoNoAceptaSobrecupoError,
)

HORA_CONSULTA = datetime.now(timezone.utc)

# --- REGLA 1: PREVENCIÓN DE CITAS DUPLICADAS ---

def test_permite_agendar_una_cita_normal_cuando_el_horario_esta_libre():
    sistema = SistemaGestionCitas()
    paciente = Paciente("Roberto Hernández")
    cita = sistema.agendar_cita(paciente, HORA_CONSULTA)
    assert cita["estado"] == "CONFIRMADA"

def test_bloquea_el_registro_si_el_paciente_intenta_agendar_dos_veces_a_la_misma_hora():
    sistema = SistemaGestionCitas()
    paciente = Paciente("Roberto Hernández")
    sistema.agendar_cita(paciente, HORA_CONSULTA)
    with pytest.raises(CitaDuplicadaError):
        sistema.agendar_cita(paciente, HORA_CONSULTA)

def test_permite_al_mismo_paciente_agendar_otra_cita_en_un_horario_diferente():
    sistema = SistemaGestionCitas()
    paciente = Paciente("Roberto Hernández")
    sistema.agendar_cita(paciente, HORA_CONSULTA)
    segunda_cita = sistema.agendar_cita(paciente, HORA_CONSULTA + timedelta(hours=2))
    assert segunda_cita["estado"] == "CONFIRMADA"

# --- REGLA 2: CONTROL DE PACIENTES CON NO-SHOWS RECURRENTES ---

def test_paciente_con_pocas_faltas_puede_seguir_agendando_por_whatsapp():
    sistema = SistemaGestionCitas()
    paciente = Paciente("Alejandro Martínez", inasistencias_previas=1)
    cita = sistema.agendar_cita(paciente, HORA_CONSULTA, canal="WHATSAPP")
    assert cita["canal"] == "WHATSAPP"

def test_paciente_con_3_faltas_acumuladas_se_le_prohibe_agendar_por_whatsapp():
    sistema = SistemaGestionCitas()
    paciente = Paciente("Danna Rodríguez", inasistencias_previas=3)
    with pytest.raises(CanalWhatsAppBloqueadoError):
        sistema.agendar_cita(paciente, HORA_CONSULTA, canal="WHATSAPP")

def test_paciente_con_3_faltas_si_puede_agendar_si_va_a_recepcion_y_paga_por_adelantado():
    sistema = SistemaGestionCitas()
    paciente = Paciente("Danna Rodríguez", inasistencias_previas=3)
    cita = sistema.agendar_cita(paciente, HORA_CONSULTA, canal="PRESENCIAL", pago_anticipado=True)
    assert cita["estado"] == "CONFIRMADA"

# --- REGLA 3: RESTRICCIÓN DE SOBRECUPOS POR MÉDICO ---

def test_permite_sobrecupo_si_el_doctor_lo_autoriza_y_hay_lugar():
    sistema = SistemaGestionCitas()
    dr = Medico("Dr. Garza", permite_sobrecupo=True)
    paciente = Paciente("Carlos López")
    res = sistema.agendar_sobrecupo(dr, paciente)
    assert "Sobrecupo asignado" in res

def test_impide_agendar_un_tercer_sobrecupo_cuando_el_doctor_ya_tiene_dos():
    sistema = SistemaGestionCitas()
    dr = Medico("Dr. Garza", permite_sobrecupo=True)
    dr.sobrecupos_actuales = 2
    paciente = Paciente("María Gómez")
    with pytest.raises(LimiteSobrecupoAlcanzadoError):
        sistema.agendar_sobrecupo(dr, paciente)

def test_impide_agendar_sobrecupo_con_doctores_que_no_lo_tienen_permitido():
    sistema = SistemaGestionCitas()
    dr = Medico("Dr. Treviño", permite_sobrecupo=False)
    paciente = Paciente("Ana Torres")
    with pytest.raises(MedicoNoAceptaSobrecupoError):
        sistema.agendar_sobrecupo(dr, paciente)
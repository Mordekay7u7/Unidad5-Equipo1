Aquí tienes el archivo **`README.md`** completo en formato Markdown listo para copiar y guardar en la raíz de tu proyecto (`Proyecto_Python_Base_U5/`).

Cubre los comandos de instalación, ejecución de pruebas, medición de cobertura, linteo, estructura del proyecto y explicación de la arquitectura de la solución de **MediNova**:

```markdown
# Sistema de Gestión de Pedidos y Citas Médicas (MediNova)
## Unidad 5 · Integración, Pruebas y Calidad de Software

Este repositorio contiene la implementación automatizada de pruebas unitarias, de integración, simulación mediante Mocks y políticas de seguridad para las reglas de negocio del proyecto base y la adaptación al dominio de la clínica **MediNova**.

---

## 🚀 Requisitos Previos

* **Python 3.11** o superior instalado.
* **Git** para el control de versiones.
* Editor de código (por ejemplo, **VS Code**).

---

## 🛠️ Instalación y Configuración del Entorno

Sigue estos pasos en tu terminal para preparar el entorno virtual e instalar las dependencias necesarias:

### 1. Clonar el repositorio e ingresar a la carpeta
```bash
git clone <URL_DE_TU_REPOSITORIO>
cd Proyecto_Python_Base_U5

```

### 2. Crear y activar el entorno virtual (`venv`)

* **Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1

```


* **macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate

```



### 3. Instalar dependencias

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

```

---

## 🧪 Ejecución de Pruebas Automatizadas

El proyecto utiliza `pytest` para la localización y ejecución de la suite de pruebas.

### 1. Ejecutar toda la suite de pruebas (Proyecto Base + MediNova)

```bash
python -m pytest -v

```

### 2. Ejecutar las pruebas del dominio MediNova con salida legible (Modo Negocio)

```bash
python -m pytest tests/test_medinova_sencillo.py -v -s

```

### 3. Ejecutar módulos individuales de prueba

* **Pruebas de Dominio / TDD:** `python -m pytest tests/test_order.py -v`
* **Persistencia (SQLAlchemy / SQLite):** `python -m pytest tests/test_repository.py -v`
* **Mocks / Pasarela de Pagos:** `python -m pytest tests/test_service.py -v`
* **Seguridad / Autorizaciones:** `python -m pytest tests/test_security.py -v`

---

## 📊 Cobertura de Código y Calidad (Linter)

### 1. Verificación del Linter (`Ruff`)

Para asegurar la calidad del código, estándares de estilo e imports ordenados:

```bash
python -m ruff check src tests

```

*(Si hay errores de formato, pueden corregirse automáticamente con `python -m ruff check src tests --fix`)*

### 2. Generar Reporte de Cobertura de Pruebas (≥80%)

Para verificar la cobertura de líneas de código y generar el reporte HTML:

```bash
python -m pytest -v --cov=src --cov-report=term-missing --cov-report=html --cov-fail-under=80

```

> **Ver Reporte HTML:** Abre el archivo `htmlcov/index.html` en cualquier navegador web para revisar el detalle de líneas instrumentadas.

---

## 🏛️ Estructura del Proyecto y Arquitectura

```text
Proyecto_Python_Base_U5/
├── .github/
│   └── workflows/
│       └── ci.yml             # Pipeline automatizado de GitHub Actions
├── src/
│   ├── domain.py              # Reglas de negocio del pedido (TDD)
│   ├── application.py         # Servicio de aplicación (Checkout / Mocks)
│   ├── repository.py          # Persistencia ORM con SQLAlchemy y SQLite
│   └── security.py           # Políticas de autorización y límites de tiempo
├── tests/
│   ├── test_order.py          # Pruebas unitarias de dominio
│   ├── test_repository.py     # Pruebas de integración DB (commit/rollback)
│   ├── test_service.py        # Pruebas con doubles/mocks de pasarela
│   ├── test_security.py       # Pruebas de políticas de cancelación
│   └── test_medinova_sencillo.py # Pruebas del PIA en lenguaje sencillo
├── casos_de_prueba_medinova.csv # Matriz de 9 casos de prueba reales del PIA
├── .gitignore                 # Archivos excluidos del control de versiones
├── requirements.txt           # Dependencias del proyecto (pytest, SQLAlchemy, ruff)
└── README.md                  # Manual de instrucciones y documentación

```

---

## ⚙️ Integración Continua (Pipeline CI)

El archivo `.github/workflows/ci.yml` automatiza las siguientes etapas en cada `push` o `pull_request` a la rama `main`:

1. **Setup:** Descarga de máquina virtual Ubuntu y configuración de Python 3.11.
2. **Dependencies:** Instalación de librerías desde `requirements.txt`.
3. **Linting:** Análisis estático de código mediante `Ruff`.
4. **Testing & Coverage:** Ejecución de `pytest` validando un umbral estricto del **80% de cobertura** mínimo sobre la carpeta `src/`.

```

```
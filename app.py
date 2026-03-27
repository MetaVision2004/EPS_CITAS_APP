import os

from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from models.pacientes import Paciente
from models.citas import Cita

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

# Mapeo de Direcciones por EPS
DIRECCIONES_EPS = {
    'Sura': 'Calle 50 # 45-20, Medellín',
    'Sanitas': 'Calle 100 # 11-60, Bogotá',
    'Nueva EPS': 'Carrera 45 # 95-12, Bogotá',
    'Compensar': 'Avenida 68 # 49-47, Bogotá',
    'Salud Total': 'Calle 10 # 50-30, Cali',
    'Coosalud': 'Carrera 20 # 30-15, Cartagena',
    'Famisanar': 'Calle 72 # 10-03, Bogotá',
    'Cafesalud': 'Avenida El Dorado # 68-15, Bogotá',
    'Medimás': 'Calle 26 # 69-76, Bogotá',
    'Coomeva': 'Calle 13 # 58-35, Cali',
    'Mutual Ser': 'Barrio Getsemaní, Cartagena'
}

# ─── Inicio ────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')

# ─── Pacientes ─────────────────────────────────────────────────────────────────

@app.route('/registro_paciente', methods=['GET', 'POST'])
def registro_paciente():
    if request.method == 'POST':
        documento  = request.form['documento'].strip()
        nombre     = request.form['nombre'].strip()
        apellido   = request.form['apellido'].strip()
        telefono   = request.form['telefono'].strip()
        correo     = request.form['correo'].strip()
        eps        = request.form['eps'].strip()

        if not all([documento, nombre, apellido, telefono, correo, eps]):
            flash('Todos los campos son obligatorios.', 'danger')
            return render_template('registro_paciente.html')

        if Paciente.existe(documento):
            flash('Ya existe un paciente registrado con ese documento.', 'warning')
            return render_template('registro_paciente.html')

        try:
            Paciente.registrar(documento, nombre, apellido, telefono, correo, eps)
            flash('¡Paciente registrado exitosamente!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Error al registrar paciente: {str(e)}', 'danger')

    return render_template('registro_paciente.html')

# ─── Citas ─────────────────────────────────────────────────────────────────────

@app.route('/reservar_cita', methods=['GET', 'POST'])
def reservar_cita():
    if request.method == 'POST':
        documento     = request.form['documento'].strip()
        medico        = request.form['medico'].strip()
        tipo_cita     = request.form['tipo_cita']
        fecha         = request.form['fecha']
        hora          = request.form['hora']
        eps = request.form.get('eps', '').strip()

        if not all([documento, medico, tipo_cita, fecha, hora, eps]):
            flash('Todos los campos son obligatorios.', 'danger')
            return render_template('reservar_cita.html')

        if not Paciente.existe(documento):
            flash('No existe un paciente con ese número de documento. Regístrelo primero.', 'warning')
            return render_template('reservar_cita.html')

        paciente = Paciente.obtener_por_documento(documento)
        paciente_eps = paciente.get('eps') if paciente else None

        # Determinar dirección de EPS en backend (campo removido de UI)
        direccion_eps = DIRECCIONES_EPS.get(eps) or DIRECCIONES_EPS.get(paciente_eps, '')

        try:
            estado = 'Pendiente'
            Cita.reservar(documento, medico, tipo_cita, fecha, hora, direccion_eps, estado)
            flash('¡Cita reservada exitosamente!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Error al reservar cita: {str(e)}', 'danger')

    return render_template('reservar_cita.html')

@app.route('/consulta_cita', methods=['GET', 'POST'])
def consulta_cita():
    if request.method == 'POST':
        documento = request.form['documento'].strip()
        if not documento:
            flash('Ingrese un número de documento.', 'danger')
            return render_template('consulta_cita.html')

        try:
            resultados = Cita.consultar(documento)
            if not resultados:
                flash('No se encontraron citas para ese documento.', 'warning')
                return render_template('consulta_cita.html')

            return render_template('resultado_cita.html', citas=resultados)
        except Exception as e:
            flash(f'Error al consultar citas: {str(e)}', 'danger')
            return render_template('consulta_cita.html')

    return render_template('consulta_cita.html')

@app.route('/api/direccion_eps/<documento>')
def api_direccion_eps(documento):
    paciente = Paciente.obtener_por_documento(documento)
    if paciente:
        eps = paciente.get('eps')
        direccion = DIRECCIONES_EPS.get(eps, 'Dirección no disponible')
        return {'success': True, 'direccion': direccion, 'eps': eps}
    return {'success': False, 'message': 'Paciente no encontrado'}

@app.route('/actualizar_cita/<int:cita_id>', methods=['GET', 'POST'])
def actualizar_cita(cita_id):
    cita = Cita.obtener_por_id(cita_id)
    if not cita:
        flash('Cita no encontrada.', 'danger')
        return redirect(url_for('consulta_cita'))

    if request.method == 'POST':
        medico    = request.form['medico'].strip()
        tipo_cita = request.form['tipo_cita']
        fecha     = request.form['fecha']
        hora      = request.form['hora']

        if not all([medico, tipo_cita, fecha, hora]):
            flash('Todos los campos son obligatorios.', 'danger')
            return render_template('actualizar_cita.html', cita=cita)

        try:
            estado = request.form.get('estado', 'Pendiente')
            Cita.actualizar(cita_id, medico, tipo_cita, fecha, hora, estado)
            flash('¡Cita actualizada exitosamente!', 'success')
            return redirect(url_for('consulta_cita'))
        except Exception as e:
            flash(f'Error al actualizar cita: {str(e)}', 'danger')

    return render_template('actualizar_cita.html', cita=cita)

# ─── Main ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=False)

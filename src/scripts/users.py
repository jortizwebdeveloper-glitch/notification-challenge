import random

from sqlalchemy import delete
from sqlalchemy.orm import Session

from src.core.db import engine
from src.core.db.models import AuthModel, NotificationModel, UserModel
from src.shared.auth import create_hash

USERS_MOKCS = [
    {"email": "jortiz@mail.com", "password": "123456"},
    {"email": "imunoz@mail.com", "password": "654231"},
    {"email": "jiom@mail.com", "password": "456789"},
]

NOTIFICATION_MOCKS: list[dict] = [
    {
        "title": "Bienvenido a la plataforma",
        "content": "# ¡Bienvenido a la plataforma!\n\nGracias por registrarte. Estamos felices de tenerte con nosotros.\n\n## Primeros pasos\n\n1. **Completa tu perfil:** agrega tu nombre, foto y preferencias.\n2. **Verifica tu correo:** así protegemos tu cuenta.\n3. **Explora el panel:** conoce las herramientas principales.\n\n## Lo que puedes hacer\n\n| Función | Descripción |\n|---|---|\n| Panel | Resumen de tu actividad |\n| Proyectos | Crea y organiza tu trabajo |\n| Ajustes | Controla tu privacidad y notificaciones |\n\n> **Consejo:** un perfil completo te ayuda a aprovechar mejor la plataforma.\n\n[Completar mi perfil](https://ejemplo.com/perfil)\n\nSi tienes dudas, escríbenos a soporte@ejemplo.com.\n\nUn saludo,\n\n**El equipo**",
        "channel": "email",
    },
    {
        "title": "Verifica tu correo",
        "content": "# Verifica tu correo electrónico\n\nPara activar tu cuenta necesitamos confirmar que esta dirección es tuya.\n\n## Cómo hacerlo\n\n1. Haz clic en el enlace de abajo.\n2. Inicia sesión si te lo solicitamos.\n3. Verás un mensaje de confirmación.\n\n[Verificar mi cuenta](https://ejemplo.com/verificar)\n\n## Importante\n\n- El enlace **vence en 24 horas**.\n- Si no creaste esta cuenta, puedes ignorar este mensaje.\n- Nunca compartas este enlace con otras personas.\n\n> ¿El enlace no funciona? Copia y pega esta dirección en tu navegador: https://ejemplo.com/verificar\n\nGracias,\n\n**El equipo de seguridad**",
        "channel": "email",
    },
    {
        "title": "Nuevo inicio de sesión",
        "content": "Detectamos un inicio de sesión desde un dispositivo nuevo en Bogotá.",
        "channel": "push",
    },
    {
        "title": "Código de verificación",
        "content": "Tu código de verificación es 482913. Expira en 10 minutos. Si no solicitaste este código, ignora este mensaje y no lo compartas con nadie.",
        "channel": "sms",
    },
    {
        "title": "Pago recibido",
        "content": "# Pago recibido\n\nRecibimos tu pago correctamente. Gracias por tu compra.\n\n## Detalle de la transacción\n\n| Concepto | Valor |\n|---|---|\n| Pedido | #10234 |\n| Monto pagado | $59.900 |\n| Método de pago | Tarjeta de crédito |\n| Estado | Aprobado |\n\n## Qué sigue\n\n- Prepararemos tu pedido en las próximas horas.\n- Te avisaremos cuando salga de bodega.\n- Podrás descargar tu factura desde tu cuenta.\n\n[Ver mi pedido](https://ejemplo.com/pedidos/10234)\n\nGuarda este correo como comprobante.\n\n**El equipo de ventas**",
        "channel": "email",
    },
    {
        "title": "Tu pedido fue enviado",
        "content": "El pedido #10234 está en camino. Llegará en 2 a 3 días hábiles.",
        "channel": "push",
    },
    {
        "title": "Recordatorio de cita",
        "content": "Recordatorio: tienes una cita mañana a las 9:00 a. m. en la sede principal. Responde CONFIRMAR para asistir o CANCELAR para reprogramar.",
        "channel": "sms",
    },
    {
        "title": "Contraseña actualizada",
        "content": "# Tu contraseña fue actualizada\n\nTe confirmamos que la contraseña de tu cuenta se cambió correctamente.\n\n## Detalle del cambio\n\n| Acción | Estado |\n|---|---|\n| Cambio de contraseña | Completado |\n| Sesiones activas | Se mantienen abiertas |\n\n## ¿No fuiste tú?\n\nSi no hiciste este cambio, actúa de inmediato:\n\n1. Restablece tu contraseña desde [este enlace](https://ejemplo.com/recuperar).\n2. Cierra todas las sesiones activas.\n3. Contáctanos en soporte@ejemplo.com.\n\n## Recomendaciones de seguridad\n\n- Usa una contraseña **única** para cada servicio.\n- Combina letras, números y símbolos.\n- Activa la verificación en dos pasos.\n\n> Nunca te pediremos tu contraseña por correo ni por teléfono.\n\n**El equipo de seguridad**",
        "channel": "email",
    },
    {
        "title": "Nuevo mensaje",
        "content": "Ana te envió un mensaje: '¿Revisaste el documento?'",
        "channel": "in_app",
    },
    {
        "title": "Suscripción por vencer",
        "content": "# Tu suscripción está por vencer\n\nTu plan **Pro** vence en **5 días**. Renuévalo para no perder acceso.\n\n## Lo que perderías\n\n- Proyectos ilimitados\n- Reportes avanzados\n- Soporte prioritario\n\n## Opciones de renovación\n\n| Plan | Facturación | Ventaja |\n|---|---|---|\n| Pro mensual | Cada mes | Flexibilidad |\n| Pro anual | Una vez al año | Mayor ahorro |\n\n[Renovar mi plan](https://ejemplo.com/renovar)\n\nSi ya renovaste, ignora este mensaje.\n\n**El equipo de suscripciones**",
        "channel": "email",
    },
    {
        "title": "Pedido entregado",
        "content": "El pedido #10234 fue entregado. ¡Esperamos que lo disfrutes!",
        "channel": "push",
    },
    {
        "title": "Oferta especial",
        "content": "# Oferta especial: 20% de descuento\n\nPor tiempo limitado, ahorra en todos los **planes anuales**.\n\n## Beneficios\n\n- **20% de descuento** sobre el precio regular\n- Acceso a todas las funciones\n- Cambio de plan sin costo durante el primer mes\n\n## Planes incluidos\n\n| Plan | Ideal para |\n|---|---|\n| Básico | Uso personal |\n| Pro | Equipos pequeños |\n| Empresa | Organizaciones grandes |\n\n> **Válido hasta el domingo.** Se aplica automáticamente al elegir un plan anual.\n\n[Aprovechar la oferta](https://ejemplo.com/ofertas)\n\nCondiciones: no acumulable con otras promociones.\n\n**El equipo**",
        "channel": "email",
    },
    {
        "title": "Te mencionaron en un comentario",
        "content": "Carlos te mencionó en la tarea 'Diseño del login'.",
        "channel": "in_app",
    },
    {
        "title": "Intento de acceso fallido",
        "content": "Alerta de seguridad: hubo 3 intentos fallidos de inicio de sesión en tu cuenta. Si no fuiste tú, cambia tu contraseña de inmediato.",
        "channel": "sms",
    },
    {
        "title": "Factura disponible",
        "content": "# Tu factura de octubre está lista\n\nYa puedes consultar y descargar tu factura correspondiente al mes de octubre.\n\n## Resumen\n\n| Concepto | Detalle |\n|---|---|\n| Periodo | Octubre |\n| Documento | Factura electrónica |\n| Formato | PDF |\n| Estado | Disponible |\n\n## Cómo descargarla\n\n1. Ingresa a tu cuenta.\n2. Ve a la sección **Facturación**.\n3. Selecciona el periodo y pulsa **Descargar**.\n\n[Descargar factura](https://ejemplo.com/facturas)\n\nConserva este documento para tus registros contables.\n\n**El equipo de facturación**",
        "channel": "email",
    },
    {
        "title": "Tarea asignada",
        "content": "Se te asignó la tarea 'Integrar pasarela de pagos'.",
        "channel": "in_app",
    },
    {
        "title": "Mantenimiento programado",
        "content": "El servicio estará en mantenimiento el sábado de 2:00 a 4:00 a. m.",
        "channel": "push",
    },
    {
        "title": "Pago rechazado",
        "content": "# No pudimos procesar tu pago\n\nTu último intento de pago fue rechazado. Necesitamos que actualices tu método de pago para continuar.\n\n## Posibles causas\n\n- Fondos insuficientes\n- Tarjeta vencida o bloqueada\n- Datos de facturación incorrectos\n- Límite de compras en línea alcanzado\n\n## Cómo solucionarlo\n\n1. Revisa los datos de tu método de pago.\n2. Actualízalo desde tu cuenta.\n3. Reintenta el pago.\n\n[Actualizar método de pago](https://ejemplo.com/pagos)\n\n> Si no actualizas tu método de pago, tu plan podría suspenderse.\n\n¿Necesitas ayuda? Escríbenos a soporte@ejemplo.com.\n\n**El equipo de pagos**",
        "channel": "email",
    },
    {
        "title": "Nuevo seguidor",
        "content": "Laura comenzó a seguirte.",
        "channel": "in_app",
    },
    {
        "title": "Encuesta de satisfacción",
        "content": "# Cuéntanos cómo fue tu experiencia\n\nTu opinión nos ayuda a mejorar. La encuesta toma solo **2 minutos**.\n\n## Qué te preguntaremos\n\n- Qué tan fácil fue usar la plataforma\n- Qué función te resultó más útil\n- Qué podríamos mejorar\n\n## Escala de calificación\n\n| Valor | Significado |\n|---|---|\n| 1 | Muy insatisfecho |\n| 3 | Neutral |\n| 5 | Muy satisfecho |\n\n[Responder la encuesta](https://ejemplo.com/encuesta)\n\nTus respuestas son **confidenciales** y se usan solo para mejorar el servicio.\n\nGracias por tu tiempo,\n\n**El equipo**",
        "channel": "email",
    },
]

with Session(engine) as session:
    session.execute(delete(NotificationModel))
    session.execute(delete(AuthModel))
    session.execute(delete(UserModel))

    USERS_ID = []

    for item in USERS_MOKCS:
        user = UserModel(email=item["email"])
        session.add(user)
        session.flush()

        USERS_ID.append(user.id)

        auth = AuthModel(password=create_hash(item["password"]), user_id=user.id)
        session.add(auth)
        session.flush()

    for item in NOTIFICATION_MOCKS:
        notification = NotificationModel(
            title=item["title"],
            content=item["content"],
            channel=item["channel"],
            user_id=random.choice(USERS_ID),
        )
        session.add(notification)

    session.commit()

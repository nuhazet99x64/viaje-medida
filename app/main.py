from data.data_actividades import ACTIVIDADES
from data.data_alojamientos import ALOJAMIENTOS
from data.data_destinos import DESTINOS
from data.productos import productos
from flask import Flask, abort, redirect, render_template, request, url_for
from form import LoginForm

# Inicializamos la aplicación
app = Flask(__name__)
app.config["SECRET_KEY"] = "mi_clave_secreta_super_segura"


# Ruta 1: Devuelve un HTML muy básico
@app.route("/")
def home():
    return render_template(
        "index.html",
        destinos=DESTINOS,
        alojamientos=ALOJAMIENTOS,
        actividades=ACTIVIDADES,
    )


@app.route("/saludo/<name>")
def saludo(name):
    # return f"<h1>Bienvenido a Flask, {name}</h1>"
    return render_template("saludo.html", name=name)


@app.route("/multiplicar/<int:n1>/<int:n2>")
def multiplicar(n1, n2):
    return f"<p>Multiplicar {n1} x {n2} da resultado {n1 * n2}"


@app.route("/catalogo")
def catalogo():
    return render_template("catalogo.html", nombre="algo", lista_productos=productos)


@app.route("/catalogo/<int:idProducto>")
def producto(idProducto):
    if 0 <= idProducto < len(productos):
        return render_template(
            "producto.html", idProducto=idProducto, producto=productos[idProducto]
        )

    abort(404)


@app.route("/contacto", methods=["GET"])
def contacto():
    return render_template("contacto.html")


@app.route("/contacto", methods=["POST"])
def contacto_post():
    nombre = request.form.get("nombre")
    mensaje = request.form["mensaje"]
    return render_template("contacto-data.html", nombre=nombre, mensaje=mensaje)


@app.route("/filtrar")
def filtrar():
    return render_template("filtrar.html")


@app.route("/filtrar-data", methods=["GET"])
def filtrar_data():
    precio_min = request.args.get("precio_min", type=float)
    print(f"Precio mínimo: {precio_min}")
    productos_filtrados = [
        producto for producto in productos if producto["precio"] >= precio_min
    ]
    print(f"Productos filtrados: {productos_filtrados}")
    # return render_template("filtrar-data.html")
    return render_template(
        "catalogo.html", nombre="Filtrado", lista_productos=productos_filtrados
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    # validate_on_submit comprueba si la petición es POST y si se validan todos los campos.
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        print(f"El usuario es {email} con la contraseña {password}")

        return redirect(url_for("gracias"))

    return render_template("login.html", form=form)


@app.route("/gracias")
def gracias():
    return render_template("gracias.html")


@app.errorhandler(404)
def pagina_no_encontrada(e):
    return render_template("404.html"), 404


@app.route("/acerca_de_nosotros")
def nosotros():
    return render_template("acerca_de_nosotros.html")


@app.route("/buscador", methods=["GET"])
def buscador():
    return render_template(
        "buscador.html",
        destinos=DESTINOS,
        alojamientos=ALOJAMIENTOS,
        actividades=ACTIVIDADES,
    )


if __name__ == "__main__":
    # host='0.0.0.0' es VITAL en Docker para que el servidor sea accesible desde fuera del contenedor
    # debug=True hará que el servidor se reinicie automáticamente si cambias este archivo
    app.run(host="0.0.0.0", port=5000, debug=True)

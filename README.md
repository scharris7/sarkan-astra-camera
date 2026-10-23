# SARKAN — Orbbec Astra+ Lightweight ROS 2 Bridge

Puente ligero para integrar la cámara **Orbbec Astra+** en **ROS 2 Humble**, desarrollado para el proyecto **SARKAN**.

El paquete utiliza captura directa mediante **V4L2** e hilos asíncronos en Python para obtener imágenes sin depender de los SDK cerrados del fabricante.

## Contenido

- [Descripción](#descripción)
- [Hardware y requisitos](#hardware-y-requisitos)
- [Validación inicial del hardware](#validación-inicial-del-hardware)
- [Instalación](#instalación)
- [Compilación](#compilación)
- [Ejecución](#ejecución)
- [Tópicos publicados](#tópicos-publicados)
- [Visor gráfico](#visor-gráfico)

## Descripción

Antes de integrar la cámara al rover o ejecutar nodos más complejos en ROS 2, se recomienda comprobar de forma aislada que el dispositivo se reconoce correctamente y entrega un flujo de vídeo válido.

Este repositorio incluye dos ejecutables principales:

- **`astra_bridge_node`**: nodo puente de captura asíncrona.
- **`image_viewer`**: visor gráfico basado en OpenCV.

## Hardware y requisitos

- **Cámara:** Orbbec Astra+ Developer Kit.
- **Alimentación:** módulo de alimentación de 5 V.
- **Equipo anfitrión:** PC o NVIDIA Jetson con puerto USB.
- **Software:** ROS 2 Humble.
- **Herramientas de validación:** `v4l2-ctl`.

> Asegúrate de que ROS 2 Humble esté instalado y de que tu entorno esté configurado antes de compilar el paquete.

## Validación inicial del hardware

### 1. Conectar y detectar la cámara

Conecta la cámara al equipo anfitrión y verifica que Linux la reconozca:

```bash
v4l2-ctl --list-devices
```

El sistema debería mostrar los nodos de vídeo asociados a la cámara. Por ejemplo, podrían aparecer `/dev/video4` y `/dev/video5` para RGB, y `/dev/video7` a `/dev/video10` para profundidad. **Los números pueden variar según el equipo y los dispositivos conectados.**

### 2. Consultar los formatos disponibles

Consulta los formatos compatibles del nodo de profundidad correspondiente. En este ejemplo se utiliza `/dev/video7`:

```bash
v4l2-ctl -d /dev/video7 --list-formats-ext
```

### Resultado esperado

La cámara debería ofrecer formatos nativos como **Y16** y **Y12**, con una resolución de **640 × 480 a 30 FPS**, sin artefactos ni desconexiones.

> Si el nodo de profundidad no es `/dev/video7`, reemplázalo por el identificador que aparezca en tu sistema.

## Instalación

Clona el repositorio dentro del directorio `src` de tu workspace de ROS 2:

```bash
cd ~/ros2_ws/src
git clone https://github.com/scharris7/sarkan-astra-camera.git astra_custom_bridge
```

## Compilación

Desde la raíz del workspace, compila el paquete con `colcon`:

```bash
cd ~/ros2_ws
colcon build --packages-select astra_custom_bridge
source install/setup.bash
```

Si abres una terminal nueva, vuelve a cargar el entorno antes de ejecutar los nodos:

```bash
source ~/ros2_ws/install/setup.bash
```

## Ejecución

### 1. Iniciar el nodo puente

Ejecuta el nodo encargado de publicar las imágenes de color y profundidad:

```bash
ros2 run astra_custom_bridge astra_bridge_node
```

Mantén esta terminal abierta mientras utilizas los tópicos o el visor.

### 2. Verificar los tópicos publicados

En otra terminal, carga el entorno de ROS 2 y lista los tópicos disponibles:

```bash
source ~/ros2_ws/install/setup.bash
ros2 topic list
```

Deberían aparecer los siguientes tópicos:

- `/camera/color/image_raw`
- `/camera/depth/image_raw`

### 3. Abrir el visor gráfico

En otra terminal, carga el entorno y ejecuta el visor basado en OpenCV:

```bash
source ~/ros2_ws/install/setup.bash
ros2 run astra_custom_bridge image_viewer
```

## Tópicos publicados

| Tópico | Descripción |
|---|---|
| `/camera/color/image_raw` | Flujo de imágenes de color (RGB). |
| `/camera/depth/image_raw` | Flujo de imágenes de profundidad. |

---

**Proyecto:** SARKAN  
**Plataforma:** ROS 2 Humble  
**Cámara:** Orbbec Astra+

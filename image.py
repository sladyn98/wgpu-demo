import imageio.v3 as iio
from wgpu.gui.auto import WgpuCanvas, run
import pygfx as gfx


canvas = WgpuCanvas()
renderer = gfx.renderers.WgpuRenderer(canvas)
scene = gfx.Scene()


im = iio.imread("memory_base.png")

image = gfx.Image(
    gfx.Geometry(grid=gfx.Texture(im, dim=2)),
    gfx.ImageBasicMaterial(clim=(0, 255)),
)
scene.add(image)

camera = gfx.OrthographicCamera(512, 512)
camera.show_object(scene, view_dir=(0, 0, 0))

@canvas.add_event_handler("wheel")
def zoom(event):
    delta_y = event['dy']  # Get the vertical scroll amount
    camera.zoom += delta_y * 0.001  # Adjust the zoom factor as needed
    camera.update_projection_matrix()  # Update the camera to apply the new zoom level
    canvas.request_draw()

dragging = False

@canvas.add_event_handler("pointer_down")
def start_drag(event):
    global dragging
    dragging = True

@canvas.add_event_handler("pointer_up")
def stop_drag(event):
    global dragging
    dragging = False

@canvas.add_event_handler("pointer_move")
def drag(event):
    global dragging
    if not dragging:
        return
    dx = event['x'] * 0.08  # Adjust the horizontal speed as necessary
    dy = event['y'] * 0.08  # Adjust the vertical speed as necessary
    camera.position.x -= dx  # Subtract dx because moving the mouse to the right should move the camera to the left
    camera.position.y += dy  # Add dy because moving the mouse up should move the camera up
    canvas.request_draw()


def animate():
    renderer.render(scene, camera)
    canvas.request_draw()


if __name__ == "__main__":
    canvas.request_draw(animate)
    run()

from viktor import ViktorController
from viktor.geometry import SquareBeam
from viktor.views import GeometryView, GeometryResult
class Controller(ViktorController):
    label = "My Beam"
    @GeometryView("My 3D model", duration_guess=1)
    def beam_visualisation(self, params, **kwargs):
        beam = SquareBeam(length_x=0.3, length_y=0.5, length_z=3)
        return GeometryResult(beam)
from operator import attrgetter

from conjureup import controllers
from conjureup.app_config import app
from conjureup.controllers.showsteps import common
from conjureup.ui.views.steps import ShowStepsView
from conjureup.ui.widgets.step import StepForm


class ShowStepsController:

    def __init__(self):
        self.view = None

    def render(self):
        common.load_steps()
        if not app.steps:
            return self.finish()

        self.view = ShowStepsView()
        self.view.show()
        app.loop.create_task(self.show_steps())

    async def show_steps(self):
        for step in filter(attrgetter('viewable'), app.steps):
            await self.show_step(step)

        return self.finish()

    async def show_step(self, step):
        step_widget = StepForm(app, step)
        self.view.add_step(step_widget)
        await step_widget.complete.wait()
        if step_widget.sudo_input:
            app.sudo_pass = step_widget.sudo_input.value
        for field in step_widget.fields:
            app.steps_data[step.name][field.key] = field.input.value

    def finish(self):
        return controllers.use('configapps').render()


_controller_class = ShowStepsController

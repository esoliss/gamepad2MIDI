import pygame
import os
import mido


os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"

# Create a MIDI output port
output_port = mido.open_output(name='Tester 1')
#print(mido.get_output_names())

but_dic = {
    "B0": {"button":0, "off":0, "on":127, "cc":4, "actual":0},
    "B1": {"button":1, "off":0, "on":127, "cc":5, "actual":0},
    "B2": {"button":2, "off":0, "on":127, "cc":6, "actual":0},
    "B3": {"button":3, "off":0, "on":127, "cc":7, "actual":0},
    "B4": {"button":4, "off":0, "on":127, "cc":8, "actual":0},
    "B8": {"button":8, "off":0, "on":127, "cc":9, "actual":0},
    "B9": {"button":9, "off":0, "on":127, "cc":10, "actual":0},
    "B10": {"button":10, "off":0, "on":127, "cc":11, "actual":0},
    "-1,0": {"button":11, "off":0, "on":127, "cc":12, "actual":0},
    "1,0": {"button":12, "off":0, "on":127, "cc":13, "actual":0},
    "0,1": {"button":13, "off":0, "on":127, "cc":14, "actual":0},
    "0,-1": {"button":14, "off":0, "on":127, "cc":15, "actual":0},
    "0,0": {"button":15, "off":0, "on":127, "cc":16, "actual":0},
}
pygame.init()

# This is a simple class that will help us print to the screen.
# It has nothing to do with the joysticks, just outputting the
# information.
class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 25)

    def tprint(self, screen, text):
        text_bitmap = self.font.render(text, True, (0, 0, 0))
        screen.blit(text_bitmap, (self.x, self.y))
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10


def main():
    # Set the width and height of the screen (width, height), and name the window.
    screen = pygame.display.set_mode((500, 700))
    pygame.display.set_caption("Joystick example")

    # Used to manage how fast the screen updates.
    clock = pygame.time.Clock()

    # Get ready to print.
    text_print = TextPrint()

    # This dict can be left as-is, since pygame will generate a
    # pygame.JOYDEVICEADDED event for every joystick connected
    # at the start of the program.
    joysticks = {}

    done = False
    while not done:
        # Event processing step.
        # Possible joystick events: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN,
        # JOYBUTTONUP, JOYHATMOTION, JOYDEVICEADDED, JOYDEVICEREMOVED

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True  # Flag that we are done so we exit this loop.

            if event.type == pygame.JOYBUTTONDOWN:
                print("Pedal button pressed.")
                press= "B"+str(event.button)
                msg = mido.Message('control_change', control=but_dic[press]["cc"], value=but_dic[press]["actual"])
                output_port.send(msg)
                #print(but_dic[press]["actual"])
                if but_dic[press]["actual"]==but_dic[press]["off"]:
                    but_dic[press]["actual"]=but_dic[press]["on"]
                else:
                    but_dic[press]["actual"]=but_dic[press]["off"]


            if event.type == pygame.JOYHATMOTION:
                print("Pedal button pressed.")
                #ht = event.hat
                ht = joystick.get_hat(0)
                print(ht)
                press= str(ht[0])+","+str(ht[1])
                if press=="0,0":
                    print("hat off")
                else:

                    msg = mido.Message('control_change', control=but_dic[press]["cc"], value=but_dic[press]["actual"])
                    output_port.send(msg)
                    #print(but_dic[press]["actual"])
                    if but_dic[press]["actual"]==but_dic[press]["off"]:
                     but_dic[press]["actual"]=but_dic[press]["on"]
                    else:
                     but_dic[press]["actual"]=but_dic[press]["off"]

            if event.type == pygame.JOYAXISMOTION:
                #AXIS 0 knob 2 CC17
                print("Pedal axis moved.")
                axis = joystick.get_axis(0)
                axis = axis*-1
                if axis<0:
                    axis = 0
                else:
                    axis = axis*127
                
                msg = mido.Message('control_change', control=17, value=int(round(axis)))
                output_port.send(msg)
                
                #AXIS 1 knob 1 CC18
                
                axis1 = joystick.get_axis(1)
                
                if axis1<0:
                    axis1 = 0
                else:
                    axis1 = axis1*127
                
                msg = mido.Message('control_change', control=18, value=int(round(axis1)))
                output_port.send(msg)

                #AXIS 2 knob 2 CC19
                
                axis2 = joystick.get_axis(2)
                
                if axis2<0:
                    axis2 = 0
                else:
                    axis2 = axis2*127
                
                msg = mido.Message('control_change', control=19, value=int(round(axis2)))
                output_port.send(msg)

            # Handle hotplugging
            if event.type == pygame.JOYDEVICEADDED:
                # This event will be generated when the program starts for every
                # joystick, filling up the list without needing to create them manually.
                joy = pygame.joystick.Joystick(event.device_index)
                joysticks[joy.get_instance_id()] = joy
                print(f"Joystick {joy.get_instance_id()} connencted")

            if event.type == pygame.JOYDEVICEREMOVED:
                del joysticks[event.instance_id]
                print(f"Joystick {event.instance_id} disconnected")

        # Drawing step
        # First, clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.
        screen.fill((255, 255, 255))
        text_print.reset()

        # Get count of joysticks.
        joystick_count = pygame.joystick.get_count()

        text_print.tprint(screen, f"Number of joysticks: {joystick_count}")
        text_print.indent()

        # For each joystick:
        for joystick in joysticks.values():
            jid = joystick.get_instance_id()

            text_print.tprint(screen, f"Joystick {jid}")
            text_print.indent()

            # Get the name from the OS for the controller/joystick.
            name = joystick.get_name()
            text_print.tprint(screen, f"Joystick name: {name}")

            guid = joystick.get_guid()
            text_print.tprint(screen, f"GUID: {guid}")

            power_level = joystick.get_power_level()
            text_print.tprint(screen, f"Joystick's power level: {power_level}")

            # Usually axis run in pairs, up/down for one, and left/right for
            # the other. Triggers count as axes.
            axes = joystick.get_numaxes()
            text_print.tprint(screen, f"Number of axes: {axes}")
            text_print.indent()

            for i in range(axes):
                axis = joystick.get_axis(i)
                text_print.tprint(screen, f"Axis {i} value: {axis:>6.3f}")
            text_print.unindent()

            buttons = joystick.get_numbuttons()
            text_print.tprint(screen, f"Number of buttons: {buttons}")
            text_print.indent()

            for i in range(buttons):
                button = joystick.get_button(i)
                text_print.tprint(screen, f"Button {i:>2} value: {button}")
            text_print.unindent()

            hats = joystick.get_numhats()
            text_print.tprint(screen, f"Number of hats: {hats}")
            text_print.indent()

            # Hat position. All or nothing for direction, not a float like
            # get_axis(). Position is a tuple of int values (x, y).
            for i in range(hats):
                hat = joystick.get_hat(i)
                text_print.tprint(screen, f"Hat {i} value: {str(hat)}")
            text_print.unindent()

            text_print.unindent()

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # Limit to 30 frames per second.
        clock.tick(30)


if __name__ == "__main__":
    main()
    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.
    pygame.quit()
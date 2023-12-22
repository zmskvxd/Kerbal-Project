import krpc
import time


conn = krpc.connect()
vessel = conn.space_center.active_vessel
altitude = vessel.flight().surface_altitude
while altitude < 110000:
    speed = vessel.flight(vessel.orbit.body.reference_frame).speed
    altitude = vessel.flight().surface_altitude
    if speed > 0.006:
        t = time.time()
        print(speed, altitude, t)

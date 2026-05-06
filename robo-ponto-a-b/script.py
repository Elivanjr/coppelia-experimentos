from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import time

sim = RemoteAPIClient().require('sim')

roda_d = sim.getObject('/junta_2_d')
roda_e = sim.getObject('/junta_2_e')
sensor = sim.getObject('/proximitySensor')

VELOCIDADE = 5.0
DURACAO_GIRO = 2.0

girando = False
tempoGiro = 0.0

sim.stopSimulation()
sim.startSimulation()

try:
    while True:
        tempoSim = sim.getSimulationTime()

        if girando:
            sim.setJointTargetVelocity(roda_d, VELOCIDADE)
            sim.setJointTargetVelocity(roda_e, VELOCIDADE)

            if tempoSim - tempoGiro >= DURACAO_GIRO:
                girando = False
        else:
            detected, distance = sim.readProximitySensor(sensor)[:2]

            if detected and distance < 3.0:
                girando = True
                tempoGiro = tempoSim
                print("Obstaculo em 3 metros, girando...")
            else:
                sim.setJointTargetVelocity(roda_d, VELOCIDADE)
                sim.setJointTargetVelocity(roda_e, VELOCIDADE)
                print("O robô está em movimento")

        time.sleep(0.05)

finally:
    sim.setJointTargetVelocity(roda_d, 0)
    sim.setJointTargetVelocity(roda_e, 0)
    sim.stopSimulation()

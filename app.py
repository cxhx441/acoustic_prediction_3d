class Equipment():
    def __init__(self, count, eqmt_tag, path, make, model, sound_level, sound_ref_dist, tested_q, installed_q, insertion_loss, x_coord, y_coord, z_coord, hz63, hz125, hz250, hz500, hz1000, hz2000, hz4000, hz8000):
        self.count = count
        self.eqmt_tag = eqmt_tag.replace(" ", "-")
        self.path = path
        self.make = make
        self.model = model
        self.sound_level = sound_level if sound_level != None else 0
        self.sound_ref_dist = sound_ref_dist if sound_ref_dist != None else 0
        self.tested_q = tested_q
        self.installed_q = installed_q
        self.insertion_loss = insertion_loss if insertion_loss != None else 0
        self.x_coord = x_coord if x_coord != None else 0
        self.y_coord = y_coord if y_coord != None else 0
        self.z_coord = z_coord if z_coord != None else 0
        self.hz63 = hz63
        self.hz125 = hz125
        self.hz250 = hz250
        self.hz500 = hz500
        self.hz1000 = hz1000
        self.hz2000 = hz2000
        self.hz4000 = hz4000
        self.hz8000 = hz8000

class Receiver(object):
    def __init__(self, r_name, x_coord, y_coord, z_coord, sound_limit, predicted_sound_level):
        self.r_name = r_name.replace(" ", "-")
        self.x_coord = x_coord if x_coord != None else 0
        self.y_coord = y_coord if y_coord != None else 0
        self.z_coord = z_coord if z_coord != None else 0
        self.sound_limit = sound_limit
        self.predicted_sound_level = predicted_sound_level

class Barrier(object):
    def __init__(self, barrier_name, x0_coord, y0_coord, z0_coord, x1_coord, y1_coord, z1_coord):
        self.barrier_name = barrier_name.replace(" ", "-")
        self.x0_coord = x0_coord if x0_coord != None else 0
        self.y0_coord = y0_coord if y0_coord != None else 0
        self.z0_coord = z0_coord if z0_coord != None else 0
        self.x1_coord = x1_coord if x1_coord != None else 0
        self.y1_coord = y1_coord if y1_coord != None else 0
        self.z1_coord = z1_coord if z1_coord != None else 0

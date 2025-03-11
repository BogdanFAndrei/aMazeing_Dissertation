class _CellDraw:
    #both my generator and solver inherit from this to gain these draw functions
    def draw_cell(self,cell,color):
        self.draw_core(cell,color)
        self.draw_walls(cell,color)

    def draw_core(self,cell,color):
        loc = cell[0]
        self.screen.fill(color,((loc[0]*self.cell_size[0]+self.wall_size[0]+self.buffer_settings[0],
                                 loc[1]*self.cell_size[1]+self.wall_size[1]+self.buffer_settings[1]),self.core_size))
     
    def draw_walls(self,cell,color):
        #Note that cells only draw their top and right walls.
        #This prevents walls from being twice as thick as desired.
        loc = cell[0]
        wal = cell[1]
        if (wal & 0b1000):
            self.screen.fill(color,((loc[0]*self.cell_size[0]+self.wall_size[0]+self.buffer_settings[0],
                                     loc[1]*self.cell_size[1]+self.buffer_settings[1]),(self.core_size[0],
                                                                               self.wall_size[1])))
        if (wal & 0b0100):
            self.screen.fill(color,((loc[0]*self.cell_size[0]+self.cell_size[0]+self.buffer_settings[0],
                                     loc[1]*self.cell_size[1]+self.wall_size[1]+self.buffer_settings[1]),(self.wall_size[0],
                                                                                                 self.core_size[1])))
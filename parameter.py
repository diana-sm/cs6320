from dataclasses import dataclass

from connectors.database import PGConn

@dataclass
class NumParameter:
    name: str
    suffix: str
    min_val: int
    max_val: int
    default_val: int
    current_val: int
    granularity: int
    log_scale: bool
    connector: PGConn = None


    def inc(self, update_db=True):
        if self.log_scale:
            new_val = self.current_val * self.granularity
            new_val = min(new_val, self.max_val)
        else:
            new_val = self.current_val + self.granularity
            new_val = max(new_val, self.min_val)

        if (self.current_val != new_val):
            self.current_val = new_val
            if update_db:
                self.update_db_config()
        
        self.current_val = new_val

    def dec(self, update_db=True):
        if self.log_scale:
            new_val = self.current_val // self.granularity
            new_val = min(new_val, self.max_val)
        else:
            new_val = self.current_val - self.granularity
            new_val = max(new_val, self.min_val)

        if (self.current_val != new_val):
            self.current_val = new_val
            if update_db:
                self.update_db_config()

    def update_db_config(self):
        connector.param_set(self.name, f'"{self.current_val}{self.suffix}"')

    def reset(self):
        if self.current_val != self.default_val:
            self.current_val = self.default_val
            self.update_db_config()

@dataclass
class BoolParameter:
    name: str
    vals: list
    default_val=1
    current_val=1
    min_val=0
    max_val=1
    connector: PGConn = None

    def inc(self, update_db=True):
        new_val = 1
        changed_val = (self.current_val != new_val)
        if (self.current_val != new_val):
            self.current_val = new_val
            if update_db:
                self.update_db_config()

    def dec(self):
        new_val = 0
        changed_val = (self.current_val != new_val)
        if (self.current_val != new_val):
            self.current_val = new_val
            if update_db:
                self.update_db_config()

    def update_db_config(self):
        connector.param_set(self.name, self.vals[self.current_val])

    def reset(self):
        if self.current_val != self.default_val:
            self.current_val = self.default_val
            self.update_db_config()

connector = PGConn()
parameters = [
        NumParameter(name="effective_cache_size", suffix="GB",
            min_val=2, max_val=16, default_val=4, current_val=4,
            granularity=2, log_scale=True,
            connector=connector),
        NumParameter(name="default_statistics_target", suffix="",
            min_val=1, max_val=10000, default_val=100, current_val=100,
            granularity=10, log_scale=True,
            connector=connector),
        NumParameter(name="random_page_cost", suffix="",
            min_val=2, max_val=5, default_val=4, current_val=4,
            granularity=0.5, log_scale=False,
            connector=connector),
        NumParameter(name="shared_buffers", suffix="MB",
            min_val=64, max_val=512, default_val=128, current_val=128,
            granularity=2, log_scale=True,
            connector=connector),
        BoolParameter(name="fsync", vals=["off", "on"], connector=connector),
        BoolParameter(name="synchronous_commit", vals=["off", "on"], connector=connector)
]

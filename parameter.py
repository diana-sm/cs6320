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
    requires_restart: bool = False
    requires_analyze: bool = False
    throughput_distribution: dict = None


    def inc(self, update_db=True):
        if self.log_scale:
            new_val = self.current_val * self.granularity
            new_val = min(new_val, self.max_val)
        else:
            new_val = self.current_val + self.granularity
            new_val = min(new_val, self.max_val)

        if (self.current_val != new_val):
            self.current_val = new_val
            if update_db:
                self.update_db_config()
        
        self.current_val = new_val

    def dec(self, update_db=True):
        if self.log_scale:
            new_val = self.current_val // self.granularity
            new_val = max(new_val, self.min_val)
        else:
            new_val = self.current_val - self.granularity
            new_val = max(new_val, self.min_val)

        if (self.current_val != new_val):
            self.current_val = new_val
            if update_db:
                self.update_db_config()

    def update_db_config(self):
        self.connector.param_set(self.name, f'"{self.current_val}{self.suffix}"')
        if self.requires_restart:
            self.connector.restart()
        if self.requires_analyze:
            self.connector.analyze()
        self.connector.show_value(self.name)

    def reset(self, update_db):
        if self.current_val != self.default_val:
            self.current_val = self.default_val
            if update_db:
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
    requires_restart: bool = False

    def inc(self, update_db=True):
        new_val = 1
        changed_val = (self.current_val != new_val)
        if (self.current_val != new_val):
            self.current_val = new_val
            if update_db:
                self.update_db_config()

    def dec(self, update_db=True):
        new_val = 0
        changed_val = (self.current_val != new_val)
        if (self.current_val != new_val):
            self.current_val = new_val
            if update_db:
                self.update_db_config()

    def update_db_config(self):
        self.connector.param_set(self.name, self.vals[self.current_val])
        if self.requires_restart:
            self.connector.restart()
        self.connector.show_value(self.name)

    def reset(self, update_db=True):
        if self.current_val != self.default_val:
            self.current_val = self.default_val
            if update_db:
                self.update_db_config()


def create_parameters(connector):
    return [
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
            min_val=32, max_val=512, default_val=128, current_val=128,
            granularity=8, log_scale=True,
            connector=connector, requires_restart=True,
            throughput_distribution = {32: (374, 8.4), 512: (407, 19.7)}),
        NumParameter(name="work_mem", suffix="MB",
            min_val=1, max_val=512, default_val=4, current_val=4,
            granularity=2, log_scale=True,
            connector=connector),
        NumParameter(name="maintenance_work_mem", suffix="MB",
            min_val=16, max_val=512, default_val=64, current_val=64,
            granularity=2, log_scale=True,
            connector=connector),
        NumParameter(name="autovacuum_vacuum_scale_factor", suffix="",
            min_val=0.1, max_val=0.4, default_val=0.2, current_val=0.2,
            granularity=0.1, log_scale=False,
            connector=connector),
        NumParameter(name="autovacuum_vacuum_threshold", suffix="",
            min_val=20, max_val=100, default_val=50, current_val=50,
            granularity=10, log_scale=False,
            connector=connector),
        BoolParameter(name="fsync", vals=["off", "on"], connector=connector),
        BoolParameter(name="synchronous_commit", vals=["off", "on"], connector=connector)
    ]

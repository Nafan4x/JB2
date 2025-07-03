import asyncio
import logging
from transitions import Machine
from logger import CustomLogger
from logic.registration import states as reg_states, transitions as reg_transitions


class FSM:
    all_states = list(set(reg_states))
    all_transitions = reg_transitions

    def __init__(self, user_id, db, state="start"):
        self.user_id = user_id
        self.state = state
        self.db = db

        self.logger = CustomLogger(
            "fsm",
            f"fsm_{user_id}.log",
            console_level=logging.INFO,
            file_level=logging.DEBUG,
        ).get_logger()

        self.machine = Machine(
            model=self,
            states=FSM.all_states,
            transitions=FSM.all_transitions,
            initial=state,
            auto_transitions=False,
        )

        self.logger.debug(f"FSM created with initial state '{self.state}'")

    def after_state_change(self):
        self.logger.info(f"User {self.user_id} state changed to {self.state}")
        # Асинхронно сохранить состояние в БД
        asyncio.create_task(self.save_state())

    async def save_state(self):
        await self.db.save_state(self.user_id, self.state)
        self.logger.debug(f"User {self.user_id} state saved to DB: {self.state}")

    async def load_state(self):
        state = await self.db.get_state(self.user_id)
        if state and state in FSM.all_states:
            self.state = state
            self.machine.set_state(state)
            self.logger.info(f"User {self.user_id} state loaded from DB: {state}")
        else:
            self.logger.info(
                f"No saved state for user {self.user_id}, using default '{self.state}'"
            )
        return self.state

    async def set_arg(self, arg: str, value):
        await self.db.set_arg(self.user_id, arg, value)

    async def get_user_data(self):
        return await self.db.get_user_data(self.user_id)

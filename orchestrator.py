class Orchestrator:

    def __init__(self, intent_service, llm_service, banking_service):
        self.intent_service = intent_service
        self.llm_service = llm_service
        self.banking_service = banking_service

    def handle(self, request, session_manager):
        message = request.message
        chat_id = request.chat_id
        phone = request.phone_number

        # 1. check workflow first
        session = session_manager.get(chat_id)

        if session:
            return self._handle_workflow(session, request, session_manager)

        # 2. intent detection
        intent = self.intent_service.detect(message)

        # 3. route
        return self._route(intent, request, session_manager)
import queue
from jupyter_client import manager


class KernelClient():
    """Wrapper implementation of jupyter_client.
    Initial reference: https://git.io/fN2T2 (gist by @abalter)
    """

    def __init__(self):
        self.kernel_manager, self.kernel_client = manager.start_new_kernel()

    def execute(self, code_string):
        req_msg_id = self.kernel_client.execute(code_string)
        execute_reply = self.kernel_client.get_shell_msg(req_msg_id)

        io_message_content = self.kernel_client.get_iopub_msg(timeout=0)['content']
        if io_message_content.get('execution_state', None) == 'idle':
            return None

        while True:
            message_content = io_message_content

            try:
                io_message_content = self.kernel_client.get_iopub_msg(timeout=0)['content']
                if io_message_content.get('execution_state', None) == 'idle':
                    break
            except queue.Empty:
                break

        if 'data' in message_content:
            result = message_content['data']['text/plain']
        elif message_content.get('name', '') == 'stdout':
            result = message_content['text']
        elif 'traceback' in message_content:
            result = '\n'.join(message_content['traceback'])
        else:
            result = ''

        return result

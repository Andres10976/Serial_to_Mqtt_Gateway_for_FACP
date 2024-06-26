#Panel de alarma de incendios Edwards IO 1000
from collections import OrderedDict
from datetime import datetime
from numpy import random
from classes.serial_port_handler import SerialPortHandler
from classes.utils import SafeQueue
import re
import time
import serial

class Specific_Serial_Handler_Template(SerialPortHandler):
    def __init__(self, config: dict, eventSeverityLevels: dict, queue: SafeQueue):
        super().__init__(config, eventSeverityLevels, queue)
        #Esto se considera, en caso de que exista un delimitador claro en cada reporte
        self.report_delimiter = "Set the delimiter"
        self.max_report_delimiter_count = 4 # configurarlo acorde a la cantidad de apariciones del delimitador por reporte 
        

    def parse_string_event(self,event: str) -> OrderedDict:
        '''
        #Extraer lo siguientes valores mediante el parseo del dato:
        ID_Event = ''
        Fecha_Panel = ''
        metadata = ''

        #El resultado que se tiene que generar:
        event_data = OrderedDict([
            ("ID_Cliente", self.config["cliente"]["id_cliente"]),
            ("ID_Panel", self.config["cliente"]["id_panel"]),
            ("Modelo_Panel", self.config["cliente"]["modelo_panel"]),
            ("ID_Modelo_Panel", self.config['cliente']['id_modelo_panel']),
            ("Mensaje", ID_Event),
            ("Tipo", "Evento"),
            ("Nivel_Severidad", self.eventSeverityLevels[ID_Event] if ID_Event in self.eventSeverityLevels else self.default_event_severity_not_recognized),
            ("Fecha_SBC", datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")),
            ("Fecha_Panel", Fecha_Panel),
            ("Metadata", metadata),
            ("uniq", random.rand())
        ])
        return event_data
        '''
        pass

#Las siguientes funciones podrian o podrian no necesitar ser sobreescritas con respecto a la clase padre
'''
    def process_incoming_data(self) -> None:
        pass

    def handle_data_line(self, incoming_line: str, buffer: str, report_count: int) -> Tuple[str, int]:
        pass

    def handle_empty_line(self, buffer: str, report_count: int) -> bool:
        pass
'''

class Edwards_iO1000(SerialPortHandler):
    def __init__(self, config: dict, eventSeverityLevels: dict, queue: SafeQueue):
        super().__init__(config, eventSeverityLevels, queue)
        self.report_delimiter = "-----------------"
        self.max_report_delimiter_count = 4

    def parse_string_event(self,event: str) -> OrderedDict:
        metadata = ""
        try:
            lines = list(filter(None, event.strip().split('\n')))
            if not lines:
                self.logger.error(f"Evento inválido recibido: {event}")
                return None

            primary_data = lines[0].split('|')
            if len(primary_data) < 2:
                self.logger.error(f"Evento inválido recibido: {event}")
                return None

            ID_Event = primary_data[0].strip()
            time_date_metadata = primary_data[1].strip().split()
            Fecha_Panel = f"{time_date_metadata[0]} {time_date_metadata[1]}"

            for meta in time_date_metadata[2:]:
                metadata = metadata + meta.strip() + " | "

            if len(lines) > 1:
                for line in lines[1:]:
                    metadata = metadata + line.strip() + "\n"

        except Exception as e:
            self.logger.exception("Ocurrió un error al parsear el evento: " + event)
            return None

        event_data = OrderedDict([
            ("ID_Cliente", self.config["cliente"]["id_cliente"]),
            ("ID_Panel", self.config["cliente"]["id_panel"]),
            ("Modelo_Panel", self.config["cliente"]["modelo_panel"]),
            ("ID_Modelo_Panel", self.config['cliente']['id_modelo_panel']),
            ("Mensaje", ID_Event),
            ("Tipo", "Evento"),
            ("Nivel_Severidad", self.eventSeverityLevels[ID_Event] if ID_Event in self.eventSeverityLevels else self.default_event_severity_not_recognized),
            ("Fecha_SBC", datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")),
            ("Fecha_Panel", Fecha_Panel),
            ("Metadata", metadata),
            ("uniq", random.rand()),
            ("latitud", self.config["cliente"]["coordenadas"]["latitud"]),
            ("longitud", self.config["cliente"]["coordenadas"]["longitud"])
        ])
        return event_data

class Edwards_EST3x(SerialPortHandler):
    def __init__(self, config: dict, eventSeverityLevels: dict, queue: SafeQueue):
        super().__init__(config, eventSeverityLevels, queue)
        #Esto se considera, en caso de que exista un delimitador claro en cada reporte
        self.report_delimiter = "-----------------" # configurarlo acorde al delimitador del reporte
        self.max_report_delimiter_count = 2 # configurarlo acorde a la cantidad de apariciones del delimitador por reporte
        self.end_report_delimiter = "**" # configurarlo acorde al delimitador del final del reporte

    def parse_string_event(self,event: str) -> OrderedDict:
        metadata = ""
        try:
            lines = list(filter(None, event.strip().split('\n')))
            if not lines:
                self.logger.error(f"Evento inválido recibido: {event}")
                return None

            primary_data = ""
            if lines[0][0] == "-":
                primary_data = lines[0][1:].split('-')
            else:
                primary_data = lines[0].split('::')
            if len(primary_data) < 2:
                self.logger.error(f"Evento inválido recibido: {event}")
                return None

            ID_Event = primary_data[0].strip()
            time_date_metadata = primary_data[1].strip().split()
            Fecha_Panel = f"{time_date_metadata[0]} {time_date_metadata[1]}"

            for meta in time_date_metadata[2:]:
                metadata = metadata + meta.strip() + " | "

            if len(lines) > 1:
                for line in lines[1:]:
                    metadata = metadata + line.strip() + "\n"

        except Exception as e:
            self.logger.exception("Ocurrió un error al parsear el evento: " + event)
            return None

        #El resultado que se tiene que generar:
        event_data = OrderedDict([
            ("ID_Cliente", self.config["cliente"]["id_cliente"]),
            ("ID_Panel", self.config["cliente"]["id_panel"]),
            ("Modelo_Panel", self.config["cliente"]["modelo_panel"]),
            ("ID_Modelo_Panel", self.config['cliente']['id_modelo_panel']),
            ("Mensaje", ID_Event),
            ("Tipo", "Evento"),
            ("Nivel_Severidad", self.eventSeverityLevels[ID_Event] if ID_Event in self.eventSeverityLevels else self.default_event_severity_not_recognized),
            ("Fecha_SBC", datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")),
            ("Fecha_Panel", Fecha_Panel),
            ("Metadata", metadata),
            ("uniq", random.rand()),
            ("latitud", self.config["cliente"]["coordenadas"]["latitud"]),
            ("longitud", self.config["cliente"]["coordenadas"]["longitud"])
        ])
        return event_data

    def check_last_line(self, string: str) -> bool:
        last_newline = string.rfind('\n', 0, string.rfind('\n'))
        last_line = string[last_newline+1:]
        return self.end_report_delimiter in last_line
    
    def handle_empty_line(self, buffer: str, report_count: int) -> bool:
        #self.logger.debug("Buffer: " + buffer)
        if report_count == 0 and buffer.strip() and self.check_last_line(buffer):
            self.logger.debug("Reporte vacio parseado. Saltandolo.")
            return True
        if report_count == self.max_report_delimiter_count and buffer.strip() and self.check_last_line(buffer):
            self.logger.debug("Reporte parseado.")
            self.publish_parsed_report(buffer)
            return True
        elif report_count == 0 and buffer.strip():
            #self.logger.debug("Evento parseado.")
            self.publish_parsed_event(buffer)
            return True
        else:
            return False

class Notifier_NFS320(SerialPortHandler):
    def __init__(self, config: dict, eventSeverityLevels: dict, queue: SafeQueue):
        super().__init__(config, eventSeverityLevels, queue)
        #Esto se considera, en caso de que exista un delimitador claro en cada reporte
        self.report_delimiter = "************"
        self.max_report_delimiter_count = 2 # configurarlo acorde a la cantidad de apariciones del delimitador por reporte 

    def parse_string_event(self,event: str) -> OrderedDict:
        metadata = ""
        severity = -1
        try:
            lines = list(filter(None, event.strip().split('\n')))
            if not lines:
                self.logger.error(f"Evento inválido recibido: {event}")
                return None

            primary_data = re.split(r'\s{3,}', lines[0])
            if len(primary_data) < 2:
                self.logger.error(f"Evento inválido recibido: {event}")
                return None
            if ":" in primary_data[0].strip():
                severity = 6
            ID_Event = primary_data[0].strip()
            metadata += ' / '.join(primary_data[1:]).strip()

            if len(lines) > 1:
                for line in lines[1:]:
                    metadata = metadata + line.strip() + "\n"

        except Exception as e:
            self.logger.exception("Ocurrió un error al parsear el evento: " + event)
            return None

        #El resultado que se tiene que generar:
        event_data = OrderedDict([
            ("ID_Cliente", self.config["cliente"]["id_cliente"]),
            ("ID_Panel", self.config["cliente"]["id_panel"]),
            ("Modelo_Panel", self.config["cliente"]["modelo_panel"]),
            ("ID_Modelo_Panel", self.config['cliente']['id_modelo_panel']),
            ("Mensaje", ID_Event),
            ("Tipo", "Evento"),
            ("Nivel_Severidad", severity if severity == 6 else (self.eventSeverityLevels[ID_Event] if ID_Event in self.eventSeverityLevels else self.default_event_severity_not_recognized)),
            ("Fecha_SBC", datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")),
            ("Metadata", metadata),
            ("uniq", random.rand()),
            ("latitud", self.config["cliente"]["coordenadas"]["latitud"]),
            ("longitud", self.config["cliente"]["coordenadas"]["longitud"])
        ])
        return event_data
    
    def process_incoming_data(self) -> None:
        buffer = ""
        report_count = 0
        add_blank_line = False
        try:
            while True:
                if self.ser.in_waiting > 0 or add_blank_line:
                    if add_blank_line:
                        add_blank_line = False  
                        if_eof = self.handle_empty_line(buffer, report_count)
                        if if_eof:
                            buffer = ""
                            report_count = 0
                    else:
                        raw_data = self.ser.readline()
                        incoming_line = raw_data.decode('latin-1').strip()
                        buffer, report_count = self.handle_data_line(incoming_line, buffer, report_count)
                        add_blank_line = True 
                else:
                    time.sleep(0.1)
        except (serial.SerialException, serial.SerialTimeoutException) as e:
            raise serial.Exception(str(e))
        except (TypeError, UnicodeDecodeError) as e:
            if buffer != "":
                if report_count > 0:
                    self.publish_parsed_report(buffer)
                else:
                    self.publish_parsed_event(buffer)
            raise TypeError(str(e))
        except Exception as e:
            #self.logger.exception("Fallo inesperado ocurrido: ")
            raise Exception(str(e))
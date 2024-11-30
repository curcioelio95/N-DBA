import os
import yaml
import logging.config
from typing import Optional
import logging


class LoggerSetup:
    """
    Configura il sistema di logging per l'applicazione.
    """
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LoggerSetup, cls).__new__(cls)
        return cls._instance

    def setup_logging(self, default_level: int = logging.INFO) -> None:
        """
        Configura il logging utilizzando il file di configurazione YAML.

        Args:
            default_level: Livello di logging predefinito
        """
        if self._initialized:
            return

        try:
            # Crea la directory dei log se non esiste
            log_dir = "/var/log/jetson_app"
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)

            # Carica la configurazione del logging
            config_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'config',
                'logging_config.yaml'
            )

            if os.path.exists(config_path):
                with open(config_path, 'rt') as f:
                    config = yaml.safe_load(f)
                logging.config.dictConfig(config)
            else:
                logging.basicConfig(level=default_level)
                logging.warning(
                    f"File di configurazione del logging non trovato in {config_path}. "
                    f"Utilizzando la configurazione di base."
                )

            self._initialized = True
            logging.info("Sistema di logging inizializzato con successo")

        except Exception as e:
            logging.basicConfig(level=default_level)
            logging.error(f"Errore nella configurazione del logging: {str(e)}")

    def get_logger(self, name: Optional[str] = None) -> logging.Logger:
        """
        Recupera un logger configurato.

        Args:
            name: Nome del logger da recuperare

        Returns:
            Logger configurato
        """
        if not self._initialized:
            self.setup_logging()

        return logging.getLogger(name if name else __name__)
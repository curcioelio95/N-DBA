import os
import yaml
from typing import Dict, Any
import logging


class ConfigLoader:
    """
    Gestisce il caricamento e l'accesso alle configurazioni del sistema.
    """
    _instance = None
    _config = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigLoader, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self) -> None:
        """
        Carica le configurazioni dal file YAML.
        """
        try:
            config_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'config',
                'config.yaml'
            )

            with open(config_path, 'r') as config_file:
                self._config = yaml.safe_load(config_file)

            logging.info("Configurazione caricata con successo")
        except Exception as e:
            logging.error(f"Errore nel caricamento della configurazione: {str(e)}")
            raise

    def get_config(self, module: str = None) -> Dict[str, Any]:
        """
        Recupera la configurazione completa o per un modulo specifico.

        Args:
            module: Nome del modulo di cui recuperare la configurazione

        Returns:
            Dict con la configurazione
        """
        if module:
            if module in self._config:
                return self._config[module]
            else:
                logging.error(f"Modulo {module} non trovato nella configurazione")
                raise KeyError(f"Configurazione non trovata per il modulo: {module}")
        return self._config

    def reload_config(self) -> None:
        """
        Ricarica la configurazione dal file.
        """
        self._load_config()
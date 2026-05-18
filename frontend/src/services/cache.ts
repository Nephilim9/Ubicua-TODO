const CACHE_PREFIX = 'safehome_cache_';

export const cacheService = {
  /**
   * Guarda un elemento en el almacenamiento local con un tiempo de vida (TTL)
   */
  set: (key: string, value: any, ttlMinutes: number = 5) => {
    const now = new Date();
    const item = {
      value: value,
      expiry: now.getTime() + ttlMinutes * 60000,
    };
    localStorage.setItem(`${CACHE_PREFIX}${key}`, JSON.stringify(item));
  },

  /**
   * Recupera un elemento y verifica si aún es válido
   */
  get: (key: string) => {
    const itemStr = localStorage.getItem(`${CACHE_PREFIX}${key}`);
    if (!itemStr) return null;

    const item = JSON.parse(itemStr);
    const now = new Date();

    if (now.getTime() > item.expiry) {
      localStorage.removeItem(`${CACHE_PREFIX}${key}`);
      return null;
    }
    return item.value;
  },

  /**
   * Elimina un elemento específico o limpia toda la caché del sistema
   */
  remove: (key: string) => {
    localStorage.removeItem(`${CACHE_PREFIX}${key}`);
  },

  clearAll: () => {
    Object.keys(localStorage)
      .filter(key => key.startsWith(CACHE_PREFIX))
      .forEach(key => localStorage.removeItem(key));
  }
};
/**
 * Layanan pemanggilan REST API ke backend FastAPI.
 * Menggunakan base URL dari VITE_API_URL atau default http://localhost:8000.
 */

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

async function fetchJson(endpoint, options = {}) {
  const url = `${BASE_URL}${endpoint}`;
  try {
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    const contentType = response.headers.get('content-type');
    const isJson = contentType && contentType.includes('application/json');
    const data = isJson ? await response.json() : await response.text();

    if (!response.ok) {
      let errorMessage = 'Terjadi kesalahan pada server.';
      if (response.status === 404) {
        errorMessage = data?.detail || 'Data yang dicari tidak ditemukan.';
      } else if (response.status === 422) {
        if (data?.pesan_error && Array.isArray(data.pesan_error)) {
          errorMessage = data.pesan_error.join(' | ');
        } else if (data?.detail) {
          errorMessage = typeof data.detail === 'string' ? data.detail : JSON.stringify(data.detail);
        } else {
          errorMessage = 'Input tidak valid. Silakan periksa kembali data Anda.';
        }
      } else if (data?.detail) {
        errorMessage = typeof data.detail === 'string' ? data.detail : 'Gagal memproses permintaan.';
      }
      const error = new Error(errorMessage);
      error.status = response.status;
      error.data = data;
      throw error;
    }

    return data;
  } catch (err) {
    if (err.name === 'TypeError' && err.message.includes('fetch')) {
      const connError = new Error('Server backend tidak dapat dihubungi. Pastikan backend aktif di http://localhost:8000.');
      connError.status = 0;
      throw connError;
    }
    throw err;
  }
}

export const api = {
  /** Memeriksa status kesehatan server backend */
  async checkHealth() {
    return fetchJson('/api/health');
  },

  /** Mengambil daftar semua laptop (opsional dengan filter merek, kategori, search) */
  async getLaptops(params = {}) {
    const query = new URLSearchParams();
    if (params.merek) query.append('merek', params.merek);
    if (params.kategori) query.append('kategori', params.kategori);
    if (params.q) query.append('q', params.q);

    const queryString = query.toString();
    const endpoint = queryString ? `/api/laptops?${queryString}` : '/api/laptops';
    return fetchJson(endpoint);
  },

  /** Mengambil detail lengkap 1 laptop berdasarkan ID */
  async getLaptopById(id) {
    return fetchJson(`/api/laptops/${id}`);
  },

  /** Memproses preferensi pengguna untuk menghasilkan rekomendasi laptop */
  async getRecommendations(payload) {
    return fetchJson('/api/recommendations', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  },

  /** Mengambil informasi metodologi Fuzzy Mamdani dan keterangan dataset */
  async getMethodInfo() {
    return fetchJson('/api/method-info');
  },
};

export default api;

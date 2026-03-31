import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from "axios";

const baseURL = import.meta.env.VITE_API_BASE_URL || "";

const service: AxiosInstance = axios.create({
  baseURL,
  timeout: 15000,
});

service.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

service.interceptors.response.use(
  (response: AxiosResponse) => {
    const res = response.data;
    if (res.code !== 200) {
      console.error("API Error:", res.message);
      return Promise.reject(new Error(res.message || "Error"));
    }
    return res;
  },
  (error) => {
    console.error("Request Error:", error);
    return Promise.reject(error);
  },
);

export default service;

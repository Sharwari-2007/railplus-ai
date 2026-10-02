import axios from 'axios';
import { 
  TrainData, 
  ConnectionRiskResult, 
  WhatIfSimulationResult, 
  CascadeGraphResult, 
  PlatformClash, 
  WeatherStation, 
  HistoricDay 
} from '../types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000/api';

export const api = {
  async getTrains(simDate: string = '2025-07-15'): Promise<TrainData[]> {
    const res = await axios.get(`${API_BASE_URL}/trains`, { params: { sim_date: simDate } });
    return res.data;
  },

  async getTrainById(trainId: string, simDate: string = '2025-07-15'): Promise<TrainData> {
    const res = await axios.get(`${API_BASE_URL}/trains/${trainId}`, { params: { sim_date: simDate } });
    return res.data;
  },

  async evaluateConnectionRisk(
    incomingTrainId: string, 
    connectingTrainId: string, 
    scheduledBufferMins: number = 40,
    simDate: string = '2025-07-15'
  ): Promise<ConnectionRiskResult> {
    const res = await axios.post(`${API_BASE_URL}/trains/connection-risk`, {
      incoming_train_id: incomingTrainId,
      connecting_train_id: connectingTrainId,
      scheduled_buffer_mins: scheduledBufferMins,
      sim_date: simDate
    });
    return res.data;
  },

  async runWhatIfSimulation(
    prioritizeRajdhani: boolean,
    emergencyBlockMins: number,
    emergencyBlockSection: string = 'Agra-Gwalior',
    simDate: string = '2025-07-15'
  ): Promise<WhatIfSimulationResult> {
    const res = await axios.post(`${API_BASE_URL}/simulate/what-if`, {
      prioritize_rajdhani: prioritizeRajdhani,
      emergency_block_mins: emergencyBlockMins,
      emergency_block_section: emergencyBlockSection,
      sim_date: simDate
    });
    return res.data;
  },

  async getCascadeGraph(): Promise<CascadeGraphResult> {
    const res = await axios.get(`${API_BASE_URL}/simulate/cascade-graph`);
    return res.data;
  },

  async getPlatformClashes(): Promise<PlatformClash[]> {
    const res = await axios.get(`${API_BASE_URL}/simulate/platform-clashes`);
    return res.data;
  },

  async getHistoricDays(): Promise<HistoricDay[]> {
    const res = await axios.get(`${API_BASE_URL}/weather/historic-days`);
    return res.data;
  },

  async getWeatherStations(simDate: string = '2025-07-15'): Promise<WeatherStation[]> {
    const res = await axios.get(`${API_BASE_URL}/weather/stations`, { params: { date_str: simDate } });
    return res.data;
  }
};

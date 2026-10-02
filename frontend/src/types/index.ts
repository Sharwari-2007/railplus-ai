export interface RouteJunction {
  name: string;
  code: string;
  km: number;
  lat: number;
  lon: number;
  arr: string;
  dep: string;
}

export interface WeatherImpact {
  met_station: string;
  rainfall_mm: number;
  min_temp_c: number;
  wind_speed_kmh: number;
  active_cautions: string[];
}

export interface XaiDelayFactor {
  factor: string;
  percentage: number;
}

export interface ProbabilisticEta {
  confidence_score_pct: number;
  interval_mins: number;
  status_label: string;
}

export interface EtaAnalysis {
  train_id: string;
  train_name: string;
  remaining_distance_km: number;
  base_mps: number;
  effective_speed_kmh: number;
  estimated_transit_mins: number;
  scheduled_remaining_mins: number;
  net_delay_mins: number;
  probabilistic_eta: ProbabilisticEta;
  weather_impact: WeatherImpact;
  xai_delay_breakdown: XaiDelayFactor[];
}

export interface TrainData {
  id: string;
  number: string;
  name: string;
  type: string;
  priority: number;
  max_speed: number;
  origin: string;
  destination: string;
  current_station: string;
  next_station: string;
  lat: number;
  lon: number;
  progress_pct: number;
  remaining_distance_km: number;
  section_occupancy: 'GREEN' | 'YELLOW' | 'RED';
  route_junctions: RouteJunction[];
  eta_analysis: EtaAnalysis;
}

export interface AlternativeTrain {
  train_number: string;
  train_name: string;
  dep_time: string;
  available_seats: number;
  buffer_mins: number;
}

export interface ConnectionRiskResult {
  incoming_train: string;
  connecting_train: string;
  junction: string;
  scheduled_buffer_mins: number;
  realized_buffer_mins: number;
  incoming_delay_mins: number;
  risk_level: 'SAFE' | 'MODERATE RISK' | 'HIGH RISK / MISSED';
  risk_color: string;
  risk_message: string;
  suggested_alternatives: AlternativeTrain[];
}

export interface TrainImpact {
  train_id: string;
  train_name: string;
  train_number: string;
  priority: number;
  original_delay_mins: number;
  simulated_delay_mins: number;
  delay_delta_mins: number;
  simulated_speed_kmh: number;
  confidence_score: number;
  status_label: string;
}

export interface WhatIfSimulationResult {
  simulation_parameters: {
    prioritize_rajdhani: boolean;
    emergency_block_mins: number;
    emergency_block_section: string;
    sim_date: string;
  };
  train_impacts: TrainImpact[];
  overall_corridor_efficiency: string;
}

export interface CascadeNode {
  id: string;
  label: string;
  delay: number;
  status: string;
}

export interface CascadeEdge {
  source: string;
  target: string;
  label: string;
}

export interface CascadeGraphResult {
  nodes: CascadeNode[];
  edges: CascadeEdge[];
}

export interface PlatformClash {
  junction: string;
  platform: string;
  conflicting_trains: Array<{ number: string; name: string; eta: string }>;
  overlap_duration_mins: number;
  severity: 'HIGH' | 'MODERATE' | 'LOW';
  recommendation: string;
}

export interface WeatherStation {
  station_name: string;
  lat: number;
  lon: number;
  rainfall_mm: number;
  min_temp: number;
  wind_speed: number;
  air_pressure: number;
  season: string;
}

export interface HistoricDay {
  id: string;
  label: string;
  date: string;
  type: string;
}

import request from '@/api/request'

export interface PayResponse {
  trade_no: string
  order_id: number
  order_no: string
  pay_amount: number
  pay_channel: string
  pay_url: string
  qrcode_url: string
  expire_at: number
  status: string
}

export const paymentApi = {
  /** 创建支付订单（获取二维码） */
  createPayment: (orderId: number, payChannel = 'mock_wechat') =>
    request.post<PayResponse>(`/payments/pay?order_id=${orderId}&pay_channel=${payChannel}`),

  /** 查询支付状态 */
  getPaymentStatus: (orderId: number) =>
    request.get<{ status: string; pay_time?: string }>(`/payments/${orderId}/status`),

  /** 模拟支付网关（扫码后确认） */
  mockGateway: (tradeNo: string, orderNo: string, amount: number, channel: string) =>
    request.get<{ status: string; trade_no: string; pay_time?: string }>(
      `/payments/gateway?trade_no=${tradeNo}&order_no=${orderNo}&amount=${amount}&channel=${channel}&action=pay`
    ),
}

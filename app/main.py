""" basic steps for a salary disbursement system

author: ashraf minhaj
mail  : ashraf_minhaj@yahoo.com
"""

from opentelemetry import trace, baggage
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.baggage.propagation import W3CBaggagePropagator
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter


# Configure OpenTelemetry trace provider
trace_provider = TracerProvider(resource=Resource.create({SERVICE_NAME: "ph-salary-disursement"}))
trace.set_tracer_provider(trace_provider)
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
tracer = trace.get_tracer(__name__)

# configure jaeger exporter
jaeger_exporter = JaegerExporter(
  agent_host_name="jaeger-agent-service",
  agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(
  BatchSpanProcessor(jaeger_exporter)
)

def inject_context_on_header(span, custom_key, custom_value):
    ctx = baggage.set_baggage(f"{custom_key}", f"{custom_value}")
    headers = {}
    W3CBaggagePropagator().inject(headers, ctx)
    TraceContextTextMapPropagator().inject(headers, ctx)
    span.set_attribute(f"{custom_key}", str(custom_value))

    return headers

# ------- Business logics --------

def send_salary():
    with tracer.start_as_current_span("send_salary") as span:
        employee_id = 7
        headers = inject_context_on_header(span=span, custom_key="employee_id", custom_value=employee_id)

        print("Salary Sending steps initialized")
        employee_data = get_employee_data(employee_id=7)
        to_disburse = determine_salary(current_salary=employee_data['salary'], employee_id=employee_data['id'])
        print(to_disburse)
        send_to_bank(to_disburse)
    

def get_employee_data(employee_id):
    with tracer.start_as_current_span("get_employee_data") as span:
        data = { 
            'id': 7,
            'salary': 20,
            'last_note': 'you will miss me when I am gone'
                }
        
        headers = inject_context_on_header(span=span, custom_key="employee_id", custom_value=f"{str(data)}")
        
        return data

def determine_salary(current_salary, employee_id):
    with tracer.start_as_current_span("determine_salary") as span:
        headers = inject_context_on_header(span=span, custom_key="employee_id", custom_value=employee_id)
        salary = current_salary
        salary += add_bonus(employee_id=employee_id)
        salary -= deduct_loan(employee_id=employee_id)
    
    return salary

def add_bonus(employee_id):
    with tracer.start_as_current_span("add_bonus") as span:
        bonus_amount = 0
        if employee_id == 7:
            bonus_amount = 10
            print('adding bonus')
            headers = inject_context_on_header(span=span, custom_key="bonus_amount", custom_value=bonus_amount)
            return bonus_amount
        return bonus_amount

def deduct_loan(employee_id):
    with tracer.start_as_current_span("deduct_loan_amount") as span:
        to_deduct = 0

        if employee_id == 7:
            to_deduct = 10
            print('deducting loan')
            headers = inject_context_on_header(span=span, custom_key="amount_to_deduct", custom_value=to_deduct)
            return to_deduct
        return to_deduct

def send_to_bank(to_disburse):
    with tracer.start_as_current_span("send_to_bank") as span:
        headers = inject_context_on_header(span=span, custom_key="amount_to_pay", custom_value=to_disburse)
        print(f'disbursing salary {to_disburse} Taka')


if __name__ == '__main__':
    send_salary()
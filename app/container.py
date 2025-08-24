from dependency_injector import containers, providers
from infrastructure.repos.mysql_billing_repository import MysqlBillingRepository
from infrastructure.gateways.bss_http import BssHttpGateway
from application.use_cases import GetCustomerSummaryByPhoneNumberUseCase, GetBillingHistoryByPhoneNumberUseCase

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration()
    billing_repo = providers.Factory(MysqlBillingRepository)
    bss_gateway = providers.Factory(BssHttpGateway)

    summary_usecase = providers.Factory(GetCustomerSummaryByPhoneNumberUseCase, bss_gateway=bss_gateway)
    billing_usecase = providers.Factory(GetBillingHistoryByPhoneNumberUseCase, repo=billing_repo)

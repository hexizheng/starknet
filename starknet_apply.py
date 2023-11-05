from starknet_py.net import AccountClient
from starknet_py.net.account.account import Account
from starknet_py.net.gateway_client import GatewayClient
from starknet_py.net.models.chains import StarknetChainId
from starknet_py.contract import Contract
from starknet_py.net.signer.stark_curve_signer import KeyPair, StarkCurveSigner
import trader
import logger
import time
from time import sleep
import random
from decimal import *

log=logger.getLogger("starknet")

client = GatewayClient(net="mainnet")
def get_my_account(private_key,public_key,wallet_address):
    keypair = KeyPair(private_key,
                      public_key)

    return Account(
        address=wallet_address,
        client=client,
        key_pair=keypair,
        chain=StarknetChainId.MAINNET,
    )

def get_my_account2(private_key,wallet_address):
    keypair = KeyPair.from_private_key(key=private_key)

    return Account(
        address=wallet_address,
        client=client,
        key_pair=keypair,
        chain=StarknetChainId.MAINNET,
    )

eth_contract_address = 0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7
usdc_contract_address = 0x053c91253bc9682c04929ca02ed00b3e423f6710d2ee7e0d5ebb06f3ecf368a8
mmswap_usdc_eth_lp_address=0x022b05f9396d2c48183f6deaf138a57522bcc8b35b67dee919f76403d1783136
jedis_usdc_eth_lp_address=0x04d0390b777b424e43839cd1e744799f3de6c176c7e32c1812a41dbd9c19db6a
swap10k_usdc_eth_lp_address=0x000023c72abdf49dffc85ae3ede714f2168ad384cc67d08524732acea90df325


def estimate_gas(my_account):
    # pass
    eth_contract = get_eth_contract(my_account)
    while True:
        estimated_fee = (
            eth_contract.functions["balanceOf"]
                .prepare(my_account.address, max_fee=0)
                .estimate_fee_sync(block_hash="latest")
        )
        print(estimated_fee)
        if estimated_fee.gas_price < 10571228271:
            log.info(f"gas 符合:{estimated_fee}")
            break
        else:
            log.info("gas过大，等待" + str(estimated_fee))
            sleep(3)


def get_eth_contract(my_account):
    eth_contract = Contract(
        address=eth_contract_address,
        abi=[{"name":"Uint256","size":2,"type":"struct","members":[{"name":"low","type":"felt","offset":0},{"name":"high","type":"felt","offset":1}]},{"data":[{"name":"from_","type":"felt"},{"name":"to","type":"felt"},{"name":"value","type":"Uint256"}],"keys":[],"name":"Transfer","type":"event"},{"data":[{"name":"owner","type":"felt"},{"name":"spender","type":"felt"},{"name":"value","type":"Uint256"}],"keys":[],"name":"Approval","type":"event"},{"name":"name","type":"function","inputs":[],"outputs":[{"name":"name","type":"felt"}],"stateMutability":"view"},{"name":"symbol","type":"function","inputs":[],"outputs":[{"name":"symbol","type":"felt"}],"stateMutability":"view"},{"name":"totalSupply","type":"function","inputs":[],"outputs":[{"name":"totalSupply","type":"Uint256"}],"stateMutability":"view"},{"name":"decimals","type":"function","inputs":[],"outputs":[{"name":"decimals","type":"felt"}],"stateMutability":"view"},{"name":"balanceOf","type":"function","inputs":[{"name":"account","type":"felt"}],"outputs":[{"name":"balance","type":"Uint256"}],"stateMutability":"view"},{"name":"allowance","type":"function","inputs":[{"name":"owner","type":"felt"},{"name":"spender","type":"felt"}],"outputs":[{"name":"remaining","type":"Uint256"}],"stateMutability":"view"},{"name":"permittedMinter","type":"function","inputs":[],"outputs":[{"name":"minter","type":"felt"}],"stateMutability":"view"},{"name":"initialized","type":"function","inputs":[],"outputs":[{"name":"res","type":"felt"}],"stateMutability":"view"},{"name":"get_version","type":"function","inputs":[],"outputs":[{"name":"version","type":"felt"}],"stateMutability":"view"},{"name":"get_identity","type":"function","inputs":[],"outputs":[{"name":"identity","type":"felt"}],"stateMutability":"view"},{"name":"initialize","type":"function","inputs":[{"name":"init_vector_len","type":"felt"},{"name":"init_vector","type":"felt*"}],"outputs":[]},{"name":"transfer","type":"function","inputs":[{"name":"recipient","type":"felt"},{"name":"amount","type":"Uint256"}],"outputs":[{"name":"success","type":"felt"}]},{"name":"transferFrom","type":"function","inputs":[{"name":"sender","type":"felt"},{"name":"recipient","type":"felt"},{"name":"amount","type":"Uint256"}],"outputs":[{"name":"success","type":"felt"}]},{"name":"approve","type":"function","inputs":[{"name":"spender","type":"felt"},{"name":"amount","type":"Uint256"}],"outputs":[{"name":"success","type":"felt"}]},{"name":"increaseAllowance","type":"function","inputs":[{"name":"spender","type":"felt"},{"name":"added_value","type":"Uint256"}],"outputs":[{"name":"success","type":"felt"}]},{"name":"decreaseAllowance","type":"function","inputs":[{"name":"spender","type":"felt"},{"name":"subtracted_value","type":"Uint256"}],"outputs":[{"name":"success","type":"felt"}]},{"name":"permissionedMint","type":"function","inputs":[{"name":"recipient","type":"felt"},{"name":"amount","type":"Uint256"}],"outputs":[]},{"name":"permissionedBurn","type":"function","inputs":[{"name":"account","type":"felt"},{"name":"amount","type":"Uint256"}],"outputs":[]}],
        provider=my_account,
    )
    return eth_contract

def get_usdc_contract(my_account):

    usdc_contract = Contract(
        address=usdc_contract_address,
        abi=[{"name":"Uint256","size":2,"type":"struct","members":[{"name":"low","type":"felt","offset":0},{"name":"high","type":"felt","offset":1}]},{"data":[{"name":"from_","type":"felt"},{"name":"to","type":"felt"},{"name":"value","type":"Uint256"}],"keys":[],"name":"Transfer","type":"event"},{"data":[{"name":"owner","type":"felt"},{"name":"spender","type":"felt"},{"name":"value","type":"Uint256"}],"keys":[],"name":"Approval","type":"event"},{"name":"name","type":"function","inputs":[],"outputs":[{"name":"name","type":"felt"}],"stateMutability":"view"},{"name":"symbol","type":"function","inputs":[],"outputs":[{"name":"symbol","type":"felt"}],"stateMutability":"view"},{"name":"totalSupply","type":"function","inputs":[],"outputs":[{"name":"totalSupply","type":"Uint256"}],"stateMutability":"view"},{"name":"decimals","type":"function","inputs":[],"outputs":[{"name":"decimals","type":"felt"}],"stateMutability":"view"},{"name":"balanceOf","type":"function","inputs":[{"name":"account","type":"felt"}],"outputs":[{"name":"balance","type":"Uint256"}],"stateMutability":"view"},{"name":"allowance","type":"function","inputs":[{"name":"owner","type":"felt"},{"name":"spender","type":"felt"}],"outputs":[{"name":"remaining","type":"Uint256"}],"stateMutability":"view"},{"name":"permittedMinter","type":"function","inputs":[],"outputs":[{"name":"minter","type":"felt"}],"stateMutability":"view"},{"name":"initialized","type":"function","inputs":[],"outputs":[{"name":"res","type":"felt"}],"stateMutability":"view"},{"name":"get_version","type":"function","inputs":[],"outputs":[{"name":"version","type":"felt"}],"stateMutability":"view"},{"name":"get_identity","type":"function","inputs":[],"outputs":[{"name":"identity","type":"felt"}],"stateMutability":"view"},{"name":"initialize","type":"function","inputs":[{"name":"init_vector_len","type":"felt"},{"name":"init_vector","type":"felt*"}],"outputs":[]},{"name":"transfer","type":"function","inputs":[{"name":"recipient","type":"felt"},{"name":"amount","type":"Uint256"}],"outputs":[{"name":"success","type":"felt"}]},{"name":"transferFrom","type":"function","inputs":[{"name":"sender","type":"felt"},{"name":"recipient","type":"felt"},{"name":"amount","type":"Uint256"}],"outputs":[{"name":"success","type":"felt"}]},{"name":"approve","type":"function","inputs":[{"name":"spender","type":"felt"},{"name":"amount","type":"Uint256"}],"outputs":[{"name":"success","type":"felt"}]},{"name":"increaseAllowance","type":"function","inputs":[{"name":"spender","type":"felt"},{"name":"added_value","type":"Uint256"}],"outputs":[{"name":"success","type":"felt"}]},{"name":"decreaseAllowance","type":"function","inputs":[{"name":"spender","type":"felt"},{"name":"subtracted_value","type":"Uint256"}],"outputs":[{"name":"success","type":"felt"}]},{"name":"permissionedMint","type":"function","inputs":[{"name":"recipient","type":"felt"},{"name":"amount","type":"Uint256"}],"outputs":[]},{"name":"permissionedBurn","type":"function","inputs":[{"name":"account","type":"felt"},{"name":"amount","type":"Uint256"}],"outputs":[]}],
        provider=my_account,
    )
    return usdc_contract

def get_myswap_usdc_eth_lp_contract(my_account):

    mmswap_usdc_eth_lp = Contract(
        address=mmswap_usdc_eth_lp_address,
        abi=[{"name":"Uint256","size":2,"type":"struct","members":[{"name":"low","type":"felt","offset":0},{"name":"high","type":"felt","offset":1}]},{"data":[{"name":"from_","type":"felt"},{"name":"to","type":"felt"},{"name":"value","type":"Uint256"}],"keys":[],"name":"Transfer","type":"event"},{"data":[{"name":"owner","type":"felt"},{"name":"spender","type":"felt"},{"name":"value","type":"Uint256"}],"keys":[],"name":"Approval","type":"event"},{"name":"name","type":"function","inputs":[],"outputs":[{"name":"name","type":"felt"}],"stateMutability":"view"},{"name":"symbol","type":"function","inputs":[],"outputs":[{"name":"symbol","type":"felt"}],"stateMutability":"view"},{"name":"totalSupply","type":"function","inputs":[],"outputs":[{"name":"totalSupply","type":"Uint256"}],"stateMutability":"view"},{"name":"decimals","type":"function","inputs":[],"outputs":[{"name":"decimals","type":"felt"}],"stateMutability":"view"},{"name":"balanceOf","type":"function","inputs":[{"name":"account","type":"felt"}],"outputs":[{"name":"balance","type":"Uint256"}],"stateMutability":"view"},{"name":"allowance","type":"function","inputs":[{"name":"owner","type":"felt"},{"name":"spender","type":"felt"}],"outputs":[{"name":"remaining","type":"Uint256"}],"stateMutability":"view"},{"name":"permittedMinter","type":"function","inputs":[],"outputs":[{"name":"minter","type":"felt"}],"stateMutability":"view"},{"name":"initialized","type":"function","inputs":[],"outputs":[{"name":"res","type":"felt"}],"stateMutability":"view"},{"name":"get_version","type":"function","inputs":[],"outputs":[{"name":"version","type":"felt"}],"stateMutability":"view"},{"name":"get_identity","type":"function","inputs":[],"outputs":[{"name":"identity","type":"felt"}],"stateMutability":"view"},{"name":"initialize","type":"function","inputs":[{"name":"init_vector_len","type":"felt"},{"name":"init_vector","type":"felt*"}],"outputs":[]},{"name":"transfer","type":"function","inputs":[{"name":"recipient","type":"felt"},{"name":"amount","type":"Uint256"}],"outputs":[{"name":"success","type":"felt"}]},{"name":"transferFrom","type":"function","inputs":[{"name":"sender","type":"felt"},{"name":"recipient","type":"felt"},{"name":"amount","type":"Uint256"}],"outputs":[{"name":"success","type":"felt"}]},{"name":"approve","type":"function","inputs":[{"name":"spender","type":"felt"},{"name":"amount","type":"Uint256"}],"outputs":[{"name":"success","type":"felt"}]},{"name":"increaseAllowance","type":"function","inputs":[{"name":"spender","type":"felt"},{"name":"added_value","type":"Uint256"}],"outputs":[{"name":"success","type":"felt"}]},{"name":"decreaseAllowance","type":"function","inputs":[{"name":"spender","type":"felt"},{"name":"subtracted_value","type":"Uint256"}],"outputs":[{"name":"success","type":"felt"}]},{"name":"permissionedMint","type":"function","inputs":[{"name":"recipient","type":"felt"},{"name":"amount","type":"Uint256"}],"outputs":[]},{"name":"permissionedBurn","type":"function","inputs":[{"name":"account","type":"felt"},{"name":"amount","type":"Uint256"}],"outputs":[]}],
        provider=my_account,
    )

    return mmswap_usdc_eth_lp


def get_eth_balance(my_account):
    eth_contract = get_eth_contract(my_account)
    return eth_contract.functions["balanceOf"].call_sync(my_account.address)[0]


def get_usdc_balance(my_account):
    usdc_contract = get_usdc_contract(my_account)
    return usdc_contract.functions["balanceOf"].call_sync(my_account.address)[0]


def getmyswap_contract(my_account):
    return Contract(
        address=0x010884171baf1914edc28d7afb619b40a4051cfae78a094a55d230f19e944a28,
        abi=[{"name":"Uint256","size":2,"type":"struct","members":[{"name":"low","type":"felt","offset":0},{"name":"high","type":"felt","offset":1}]},{"name":"Pool","size":10,"type":"struct","members":[{"name":"name","type":"felt","offset":0},{"name":"token_a_address","type":"felt","offset":1},{"name":"token_a_reserves","type":"Uint256","offset":2},{"name":"token_b_address","type":"felt","offset":4},{"name":"token_b_reserves","type":"Uint256","offset":5},{"name":"fee_percentage","type":"felt","offset":7},{"name":"cfmm_type","type":"felt","offset":8},{"name":"liq_token","type":"felt","offset":9}]},{"data":[{"name":"implementation","type":"felt"}],"keys":[],"name":"Upgraded","type":"event"},{"data":[{"name":"previousAdmin","type":"felt"},{"name":"newAdmin","type":"felt"}],"keys":[],"name":"AdminChanged","type":"event"},{"name":"swap","type":"function","inputs":[{"name":"pool_id","type":"felt"},{"name":"token_from_addr","type":"felt"},{"name":"amount_from","type":"Uint256"},{"name":"amount_to_min","type":"Uint256"}],"outputs":[{"name":"amount_to","type":"Uint256"}]},{"name":"withdraw_liquidity","type":"function","inputs":[{"name":"pool_id","type":"felt"},{"name":"shares_amount","type":"Uint256"},{"name":"amount_min_a","type":"Uint256"},{"name":"amount_min_b","type":"Uint256"}],"outputs":[{"name":"actual1","type":"Uint256"},{"name":"actual2","type":"Uint256"},{"name":"res1","type":"Uint256"},{"name":"res2","type":"Uint256"}]},{"name":"add_liquidity","type":"function","inputs":[{"name":"a_address","type":"felt"},{"name":"a_amount","type":"Uint256"},{"name":"a_min_amount","type":"Uint256"},{"name":"b_address","type":"felt"},{"name":"b_amount","type":"Uint256"},{"name":"b_min_amount","type":"Uint256"}],"outputs":[{"name":"actual1","type":"Uint256"},{"name":"actual2","type":"Uint256"}]},{"name":"create_new_pool","type":"function","inputs":[{"name":"pool_name","type":"felt"},{"name":"a_address","type":"felt"},{"name":"a_initial_liquidity","type":"Uint256"},{"name":"b_address","type":"felt"},{"name":"b_initial_liquidity","type":"Uint256"},{"name":"a_times_b_sqrt_value","type":"Uint256"}],"outputs":[{"name":"pool_id","type":"felt"}]},{"name":"get_version","type":"function","inputs":[],"outputs":[{"name":"ver","type":"felt"}],"stateMutability":"view"},{"name":"get_total_number_of_pools","type":"function","inputs":[],"outputs":[{"name":"num","type":"felt"}],"stateMutability":"view"},{"name":"get_pool","type":"function","inputs":[{"name":"pool_id","type":"felt"}],"outputs":[{"name":"pool","type":"Pool"}],"stateMutability":"view"},{"name":"get_lp_balance","type":"function","inputs":[{"name":"pool_id","type":"felt"},{"name":"lp_address","type":"felt"}],"outputs":[{"name":"shares","type":"Uint256"}],"stateMutability":"view"},{"name":"get_total_shares","type":"function","inputs":[{"name":"pool_id","type":"felt"}],"outputs":[{"name":"total_shares","type":"Uint256"}],"stateMutability":"view"},{"name":"upgrade","type":"function","inputs":[{"name":"new_implementation","type":"felt"}],"outputs":[]}],
        provider=my_account,
    )


def swap_myswap(my_account,amount_in):
    eth_balance = get_eth_balance(my_account)
    log.info(eth_balance)
    log.info("开始myswap eth2usdc交易："+str(amount_in))
    log.info("账户地址:" + str(hex(my_account.address)))

    amount_in = int(Decimal(str(amount_in)) * Decimal("1e18"))
    eth_contract = get_eth_contract(my_account)
    approve_call = eth_contract.functions["approve"].prepare(0x010884171baf1914edc28d7afb619b40a4051cfae78a094a55d230f19e944a28, amount_in)
    contract = Contract(
        address=0x010884171baf1914edc28d7afb619b40a4051cfae78a094a55d230f19e944a28,
        abi=[{"name":"Uint256","size":2,"type":"struct","members":[{"name":"low","type":"felt","offset":0},{"name":"high","type":"felt","offset":1}]},{"name":"Pool","size":10,"type":"struct","members":[{"name":"name","type":"felt","offset":0},{"name":"token_a_address","type":"felt","offset":1},{"name":"token_a_reserves","type":"Uint256","offset":2},{"name":"token_b_address","type":"felt","offset":4},{"name":"token_b_reserves","type":"Uint256","offset":5},{"name":"fee_percentage","type":"felt","offset":7},{"name":"cfmm_type","type":"felt","offset":8},{"name":"liq_token","type":"felt","offset":9}]},{"data":[{"name":"implementation","type":"felt"}],"keys":[],"name":"Upgraded","type":"event"},{"data":[{"name":"previousAdmin","type":"felt"},{"name":"newAdmin","type":"felt"}],"keys":[],"name":"AdminChanged","type":"event"},{"name":"swap","type":"function","inputs":[{"name":"pool_id","type":"felt"},{"name":"token_from_addr","type":"felt"},{"name":"amount_from","type":"Uint256"},{"name":"amount_to_min","type":"Uint256"}],"outputs":[{"name":"amount_to","type":"Uint256"}]},{"name":"withdraw_liquidity","type":"function","inputs":[{"name":"pool_id","type":"felt"},{"name":"shares_amount","type":"Uint256"},{"name":"amount_min_a","type":"Uint256"},{"name":"amount_min_b","type":"Uint256"}],"outputs":[{"name":"actual1","type":"Uint256"},{"name":"actual2","type":"Uint256"},{"name":"res1","type":"Uint256"},{"name":"res2","type":"Uint256"}]},{"name":"add_liquidity","type":"function","inputs":[{"name":"a_address","type":"felt"},{"name":"a_amount","type":"Uint256"},{"name":"a_min_amount","type":"Uint256"},{"name":"b_address","type":"felt"},{"name":"b_amount","type":"Uint256"},{"name":"b_min_amount","type":"Uint256"}],"outputs":[{"name":"actual1","type":"Uint256"},{"name":"actual2","type":"Uint256"}]},{"name":"create_new_pool","type":"function","inputs":[{"name":"pool_name","type":"felt"},{"name":"a_address","type":"felt"},{"name":"a_initial_liquidity","type":"Uint256"},{"name":"b_address","type":"felt"},{"name":"b_initial_liquidity","type":"Uint256"},{"name":"a_times_b_sqrt_value","type":"Uint256"}],"outputs":[{"name":"pool_id","type":"felt"}]},{"name":"get_version","type":"function","inputs":[],"outputs":[{"name":"ver","type":"felt"}],"stateMutability":"view"},{"name":"get_total_number_of_pools","type":"function","inputs":[],"outputs":[{"name":"num","type":"felt"}],"stateMutability":"view"},{"name":"get_pool","type":"function","inputs":[{"name":"pool_id","type":"felt"}],"outputs":[{"name":"pool","type":"Pool"}],"stateMutability":"view"},{"name":"get_lp_balance","type":"function","inputs":[{"name":"pool_id","type":"felt"},{"name":"lp_address","type":"felt"}],"outputs":[{"name":"shares","type":"Uint256"}],"stateMutability":"view"},{"name":"get_total_shares","type":"function","inputs":[{"name":"pool_id","type":"felt"}],"outputs":[{"name":"total_shares","type":"Uint256"}],"stateMutability":"view"},{"name":"upgrade","type":"function","inputs":[{"name":"new_implementation","type":"felt"}],"outputs":[]}],
        provider=my_account,
    )
    amount_out_min = get_amounts_out_min(my_account,amount_in)
    swap_call = contract.functions["swap"].prepare(1,0x49d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7, amount_in, amount_out_min)
    response = my_account.execute_sync([approve_call, swap_call], auto_estimate=True)
    print(str(hex(response.transaction_hash)))
    log.info("交易结果：" + str(hex(response.transaction_hash)))

def addliquidity_myswap(my_account,usdc_amount_in):
    log.info("开始myswap add liquidity交易：")
    log.info("账户地址:" + str(hex(my_account.address)))
    usdc_amount_in_min = int(usdc_amount_in/1.024)
    eth_amount_in = get_eth_amounts_out_min(my_account,usdc_amount_in)
    eth_amount_in_min = int(usdc_amount_in_min/1.024)
    eth_contract = get_eth_contract(my_account)
    eth_approve_call = eth_contract.functions["approve"].prepare(0x010884171baf1914edc28d7afb619b40a4051cfae78a094a55d230f19e944a28, eth_amount_in)
    usdc_contract = get_usdc_contract(my_account)
    usdc_approve_call = usdc_contract.functions["approve"].prepare(0x010884171baf1914edc28d7afb619b40a4051cfae78a094a55d230f19e944a28, usdc_amount_in)

    contract = getmyswap_contract(my_account)
    addliquidity_call = contract.functions["add_liquidity"].prepare(usdc_contract_address,usdc_amount_in,usdc_amount_in_min,eth_contract_address,eth_amount_in,eth_amount_in_min)
    response = my_account.execute_sync([eth_approve_call, usdc_approve_call,addliquidity_call], auto_estimate=True)
    print(str(hex(response.transaction_hash)))
    log.info("交易结果：" + str(hex(response.transaction_hash)))


def removeliquidity_myswap(my_account):
    log.info("开始myswap remove liquidity交易：")
    log.info("账户地址:" + str(hex(my_account.address)))
    contract = getmyswap_contract(my_account)
    # usdc-eth 池子 pool id 是 1
    totalshares = (contract.functions["get_total_shares"].call_sync(1)).total_shares
    myshares = (contract.functions["get_lp_balance"].call_sync(1,my_account.address)).shares
    if myshares == 0:
        print("当前没有池子，返回")
        log.info("当前没有池子， 改为加池子操作")
        addliquidity_myswap(my_account)
        return
    pool = contract.functions["get_pool"].call_sync(1)
    token_a_reserves = pool.pool['token_a_reserves']
    token_b_reserves = pool.pool['token_b_reserves']

    remove_shares = myshares
    amount_min_a = int(remove_shares*token_a_reserves/totalshares/1.02)
    amount_min_b = int(remove_shares*token_b_reserves/totalshares/1.02)


    lp_contract = get_myswap_usdc_eth_lp_contract(my_account)
    lp_approve_call = lp_contract.functions["approve"].prepare(
        0x010884171baf1914edc28d7afb619b40a4051cfae78a094a55d230f19e944a28, remove_shares)
    removeliquidity_call = contract.functions["withdraw_liquidity"].prepare(1, remove_shares,amount_min_a, amount_min_b)
    response = my_account.execute_sync([lp_approve_call, removeliquidity_call], auto_estimate=True)
    print(str(hex(response.transaction_hash)))
    log.info("交易结果：" + str(hex(response.transaction_hash)))


# usdc 换一部分成为eth
def swap_myswap_usdc2eth(my_account,amount_in):
    log.info("开始myswap 部分usdc2eth交易：")
    log.info("账户地址:" + str(hex(my_account.address)))
    log.info("开始myswap usdc2eth交易：" + str(amount_in))
    log.info("账户地址:" + str(hex(my_account.address)))

    usdc_contract = get_usdc_contract(my_account)
    approve_call = usdc_contract.functions["approve"].prepare(0x010884171baf1914edc28d7afb619b40a4051cfae78a094a55d230f19e944a28, amount_in)
    contract = getmyswap_contract(my_account)
    amount_out_min = get_eth_amounts_out_min(my_account, amount_in)
    print(amount_out_min)
    swap_call = contract.functions["swap"].prepare(1, 0x053c91253bc9682c04929ca02ed00b3e423f6710d2ee7e0d5ebb06f3ecf368a8,
                                                   amount_in, amount_out_min)

    response = my_account.execute_sync([approve_call, swap_call], auto_estimate=True)
    print(str(hex(response.transaction_hash)))
    log.info("交易结果：" + str(hex(response.transaction_hash)))


# eth 金额get usdc 金额
def get_amounts_out_min(my_account,amount_in):
    path = [
        0x49d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7,
        0x53c91253bc9682c04929ca02ed00b3e423f6710d2ee7e0d5ebb06f3ecf368a8
    ]
    contract = Contract(
        address=0x041fd22b238fa21cfcf5dd45a8548974d8263b3a531a60388411c5e230f97023,
        abi=[{"name":"Uint256","size":2,"type":"struct","members":[{"name":"low","type":"felt","offset":0},{"name":"high","type":"felt","offset":1}]},{"data":[{"name":"implementation","type":"felt"}],"keys":[],"name":"Upgraded","type":"event"},{"data":[{"name":"previousAdmin","type":"felt"},{"name":"newAdmin","type":"felt"}],"keys":[],"name":"AdminChanged","type":"event"},{"name":"initializer","type":"function","inputs":[{"name":"factory","type":"felt"},{"name":"proxy_admin","type":"felt"}],"outputs":[]},{"name":"factory","type":"function","inputs":[],"outputs":[{"name":"address","type":"felt"}],"stateMutability":"view"},{"name":"sort_tokens","type":"function","inputs":[{"name":"tokenA","type":"felt"},{"name":"tokenB","type":"felt"}],"outputs":[{"name":"token0","type":"felt"},{"name":"token1","type":"felt"}],"stateMutability":"view"},{"name":"quote","type":"function","inputs":[{"name":"amountA","type":"Uint256"},{"name":"reserveA","type":"Uint256"},{"name":"reserveB","type":"Uint256"}],"outputs":[{"name":"amountB","type":"Uint256"}],"stateMutability":"view"},{"name":"get_amount_out","type":"function","inputs":[{"name":"amountIn","type":"Uint256"},{"name":"reserveIn","type":"Uint256"},{"name":"reserveOut","type":"Uint256"}],"outputs":[{"name":"amountOut","type":"Uint256"}],"stateMutability":"view"},{"name":"get_amount_in","type":"function","inputs":[{"name":"amountOut","type":"Uint256"},{"name":"reserveIn","type":"Uint256"},{"name":"reserveOut","type":"Uint256"}],"outputs":[{"name":"amountIn","type":"Uint256"}],"stateMutability":"view"},{"name":"get_amounts_out","type":"function","inputs":[{"name":"amountIn","type":"Uint256"},{"name":"path_len","type":"felt"},{"name":"path","type":"felt*"}],"outputs":[{"name":"amounts_len","type":"felt"},{"name":"amounts","type":"Uint256*"}],"stateMutability":"view"},{"name":"get_amounts_in","type":"function","inputs":[{"name":"amountOut","type":"Uint256"},{"name":"path_len","type":"felt"},{"name":"path","type":"felt*"}],"outputs":[{"name":"amounts_len","type":"felt"},{"name":"amounts","type":"Uint256*"}],"stateMutability":"view"},{"name":"add_liquidity","type":"function","inputs":[{"name":"tokenA","type":"felt"},{"name":"tokenB","type":"felt"},{"name":"amountADesired","type":"Uint256"},{"name":"amountBDesired","type":"Uint256"},{"name":"amountAMin","type":"Uint256"},{"name":"amountBMin","type":"Uint256"},{"name":"to","type":"felt"},{"name":"deadline","type":"felt"}],"outputs":[{"name":"amountA","type":"Uint256"},{"name":"amountB","type":"Uint256"},{"name":"liquidity","type":"Uint256"}]},{"name":"remove_liquidity","type":"function","inputs":[{"name":"tokenA","type":"felt"},{"name":"tokenB","type":"felt"},{"name":"liquidity","type":"Uint256"},{"name":"amountAMin","type":"Uint256"},{"name":"amountBMin","type":"Uint256"},{"name":"to","type":"felt"},{"name":"deadline","type":"felt"}],"outputs":[{"name":"amountA","type":"Uint256"},{"name":"amountB","type":"Uint256"}]},{"name":"swap_exact_tokens_for_tokens","type":"function","inputs":[{"name":"amountIn","type":"Uint256"},{"name":"amountOutMin","type":"Uint256"},{"name":"path_len","type":"felt"},{"name":"path","type":"felt*"},{"name":"to","type":"felt"},{"name":"deadline","type":"felt"}],"outputs":[{"name":"amounts_len","type":"felt"},{"name":"amounts","type":"Uint256*"}]},{"name":"swap_tokens_for_exact_tokens","type":"function","inputs":[{"name":"amountOut","type":"Uint256"},{"name":"amountInMax","type":"Uint256"},{"name":"path_len","type":"felt"},{"name":"path","type":"felt*"},{"name":"to","type":"felt"},{"name":"deadline","type":"felt"}],"outputs":[{"name":"amounts_len","type":"felt"},{"name":"amounts","type":"Uint256*"}]}],
        provider=my_account,
    )
    out = contract.functions["get_amounts_out"].call_sync(amount_in, path)
    amount_out_min = int(out[0][1] * 0.98)
    return amount_out_min


# usdc 金额 gets eth 金额
def get_eth_amounts_out_min(my_account,amount_in):
    path = [
        0x53c91253bc9682c04929ca02ed00b3e423f6710d2ee7e0d5ebb06f3ecf368a8,
        0x49d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7
    ]
    contract = Contract(
        address=0x041fd22b238fa21cfcf5dd45a8548974d8263b3a531a60388411c5e230f97023,
        abi=[{"name":"Uint256","size":2,"type":"struct","members":[{"name":"low","type":"felt","offset":0},{"name":"high","type":"felt","offset":1}]},{"data":[{"name":"implementation","type":"felt"}],"keys":[],"name":"Upgraded","type":"event"},{"data":[{"name":"previousAdmin","type":"felt"},{"name":"newAdmin","type":"felt"}],"keys":[],"name":"AdminChanged","type":"event"},{"name":"initializer","type":"function","inputs":[{"name":"factory","type":"felt"},{"name":"proxy_admin","type":"felt"}],"outputs":[]},{"name":"factory","type":"function","inputs":[],"outputs":[{"name":"address","type":"felt"}],"stateMutability":"view"},{"name":"sort_tokens","type":"function","inputs":[{"name":"tokenA","type":"felt"},{"name":"tokenB","type":"felt"}],"outputs":[{"name":"token0","type":"felt"},{"name":"token1","type":"felt"}],"stateMutability":"view"},{"name":"quote","type":"function","inputs":[{"name":"amountA","type":"Uint256"},{"name":"reserveA","type":"Uint256"},{"name":"reserveB","type":"Uint256"}],"outputs":[{"name":"amountB","type":"Uint256"}],"stateMutability":"view"},{"name":"get_amount_out","type":"function","inputs":[{"name":"amountIn","type":"Uint256"},{"name":"reserveIn","type":"Uint256"},{"name":"reserveOut","type":"Uint256"}],"outputs":[{"name":"amountOut","type":"Uint256"}],"stateMutability":"view"},{"name":"get_amount_in","type":"function","inputs":[{"name":"amountOut","type":"Uint256"},{"name":"reserveIn","type":"Uint256"},{"name":"reserveOut","type":"Uint256"}],"outputs":[{"name":"amountIn","type":"Uint256"}],"stateMutability":"view"},{"name":"get_amounts_out","type":"function","inputs":[{"name":"amountIn","type":"Uint256"},{"name":"path_len","type":"felt"},{"name":"path","type":"felt*"}],"outputs":[{"name":"amounts_len","type":"felt"},{"name":"amounts","type":"Uint256*"}],"stateMutability":"view"},{"name":"get_amounts_in","type":"function","inputs":[{"name":"amountOut","type":"Uint256"},{"name":"path_len","type":"felt"},{"name":"path","type":"felt*"}],"outputs":[{"name":"amounts_len","type":"felt"},{"name":"amounts","type":"Uint256*"}],"stateMutability":"view"},{"name":"add_liquidity","type":"function","inputs":[{"name":"tokenA","type":"felt"},{"name":"tokenB","type":"felt"},{"name":"amountADesired","type":"Uint256"},{"name":"amountBDesired","type":"Uint256"},{"name":"amountAMin","type":"Uint256"},{"name":"amountBMin","type":"Uint256"},{"name":"to","type":"felt"},{"name":"deadline","type":"felt"}],"outputs":[{"name":"amountA","type":"Uint256"},{"name":"amountB","type":"Uint256"},{"name":"liquidity","type":"Uint256"}]},{"name":"remove_liquidity","type":"function","inputs":[{"name":"tokenA","type":"felt"},{"name":"tokenB","type":"felt"},{"name":"liquidity","type":"Uint256"},{"name":"amountAMin","type":"Uint256"},{"name":"amountBMin","type":"Uint256"},{"name":"to","type":"felt"},{"name":"deadline","type":"felt"}],"outputs":[{"name":"amountA","type":"Uint256"},{"name":"amountB","type":"Uint256"}]},{"name":"swap_exact_tokens_for_tokens","type":"function","inputs":[{"name":"amountIn","type":"Uint256"},{"name":"amountOutMin","type":"Uint256"},{"name":"path_len","type":"felt"},{"name":"path","type":"felt*"},{"name":"to","type":"felt"},{"name":"deadline","type":"felt"}],"outputs":[{"name":"amounts_len","type":"felt"},{"name":"amounts","type":"Uint256*"}]},{"name":"swap_tokens_for_exact_tokens","type":"function","inputs":[{"name":"amountOut","type":"Uint256"},{"name":"amountInMax","type":"Uint256"},{"name":"path_len","type":"felt"},{"name":"path","type":"felt*"},{"name":"to","type":"felt"},{"name":"deadline","type":"felt"}],"outputs":[{"name":"amounts_len","type":"felt"},{"name":"amounts","type":"Uint256*"}]}],
        provider=my_account,
    )
    out = contract.functions["get_amounts_out"].call_sync(amount_in, path)
    amount_out_min = int(out[0][1] * 0.98)
    return amount_out_min

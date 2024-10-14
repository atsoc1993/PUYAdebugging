from algopy import Txn, gtxn, ARC4Contract, Bytes, Account, Application, Asset, TransactionType, String, itxn, Global, OnCompleteAction, UInt64
from algopy.arc4 import abimethod, Address, arc4_signature, ARC4Client, abi_call, Tuple
from algopy.arc4 import UInt64 as arc4UInt64
from algopy.arc4 import String as arc4String

class TransactionComp(ARC4Contract):
    def __init__(self) -> None:
        pass
    
    @abimethod
    def inner_txn_comprehension(self) -> tuple[UInt64, UInt64, UInt64, UInt64, String, tuple[String, String]]:
        asset_config_txn = itxn.AssetConfig(
            total = 1,
            unit_name="TEST#1",
            asset_name="TEST ASSET ONE",
            decimals=0,
            default_frozen=False,
            manager = Global.current_application_address,
            reserve = Global.current_application_address,
            fee=Global.min_txn_fee
        ).submit()
        
        asset_config_txn_2 = itxn.AssetConfig(
            total = 1,
            unit_name="TEST#2",
            asset_name="TEST ASSET TWO",
            decimals=0,
            default_frozen=False,
            manager = Global.current_application_address,
            reserve = Global.current_application_address,
            fee=Global.min_txn_fee,
            note="Extra Transaction #2"
        )
        
        asset_config_txn_3 = itxn.AssetConfig(
            total = 1,
            unit_name="TEST#3",
            asset_name="TEST ASSET THREE",
            decimals=0,
            default_frozen=False,
            manager = Global.current_application_address,
            reserve = Global.current_application_address,
            fee=Global.min_txn_fee,
            note="Extra Transaction #3"
        )

        submit_tx_1, submit_tx_2 = itxn.submit_txns(asset_config_txn_2, asset_config_txn_3)
        
        current_app = Global.current_application_id
        approval_program = current_app.approval_program
        clear_program = current_app.clear_state_program
        create_new_app_clone_tx = itxn.ApplicationCall(
            approval_program=current_app.approval_program,
            clear_state_program=current_app.clear_state_program,
            on_completion=OnCompleteAction.NoOp,
          #  global_num_uint=0,
          #  global_num_bytes=0,
          #  local_num_bytes=0,
          #  local_num_uint=0,
            fee=Global.min_txn_fee
        ).submit()
        
        #return_nothing_signature = arc4_signature("return_nothing()string")
        
        response, transaction = abi_call[String](
            'return_nothing',
            #arguments would go here,
            app_id=create_new_app_clone_tx.created_app,
            fee=Global.min_txn_fee
        )
    
        response_2, transaction_2 = abi_call[String, String](
            'return_something_with_test_text',
            String("Something"),
            app_id=create_new_app_clone_tx.created_app,
            fee=Global.min_txn_fee
        )

        return asset_config_txn.created_asset.id, submit_tx_1.created_asset.id, submit_tx_2.created_asset.id, create_new_app_clone_tx.created_app.id, response, response_2
    
    
    @abimethod
    def return_nothing(self) -> String:
        return String("Nothing")
    
    @abimethod
    def return_something_with_test_text(self, arg: String) -> tuple[String, String]:
        return arg, String("Test")
    

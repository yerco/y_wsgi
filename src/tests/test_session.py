from src.session.session import Session
from src.session.session_memento import SessionMemento
from src.session.session_caretaker import SessionCaretaker
from src.session.session_store import SessionStore


# Mock config for testing
class Config:
    SECRET_KEY = 'test_secret_key'


config = Config()


def test_session_store_initialization():
    store = SessionStore()
    assert len(store) == 0


def test_write_and_get_session():
    store = SessionStore()
    session = Session(user_id="user1")
    session.id = 'session1'
    store.write(session)

    assert len(store) == 1
    retrieved_session = store.get_session_by_id('session1')
    assert retrieved_session.signed_id == store._sign_session_id('session1')


def test_undo_redo_functionality():
    store = SessionStore()

    # Write sessions
    session1 = Session(user_id="user1")
    session1.id = 'session1'
    store.write(session1)

    session2 = Session(user_id="user1")
    session2.id = 'session2'
    store.write(session2)

    assert len(store) == 2

    # Undo the last session
    store.undo()
    assert len(store) == 1
    assert store.get_session_by_id(session1.id).signed_id == store._sign_session_id('session1')

    # Redo the last undone session
    store.redo()
    assert len(store) == 2
    assert store.get_session_by_id(session2.id).signed_id == store._sign_session_id('session2')

    # Undo twice
    store.undo()
    store.undo()
    assert len(store) == 0

    # Redo twice
    store.redo()
    store.redo()
    assert len(store) == 2
    assert store.get_session_by_id(session2.id).signed_id == store._sign_session_id('session2')


def test_session_caretaker():
    caretaker = SessionCaretaker()

    # Initial state: No mementos
    assert caretaker.get_current_memento() is None

    session1 = Session(user_id="user1")
    memento1 = SessionMemento([session1])
    caretaker.save_memento(memento1)
    assert caretaker.get_current_memento() == memento1

    session2 = Session(user_id="user1")
    memento2 = SessionMemento([session1, session2])
    caretaker.save_memento(memento2)
    assert caretaker.get_current_memento() == memento2

    session3 = Session(user_id="user1")
    memento3 = SessionMemento([session1, session2, session3])
    caretaker.save_memento(memento3)
    assert caretaker.get_current_memento() == memento3

    # Test undo functionality
    assert caretaker.undo() == memento2
    assert caretaker.get_current_memento() == memento2

    assert caretaker.undo() == memento1
    assert caretaker.get_current_memento() == memento1

    # Test redo functionality
    assert caretaker.redo() == memento2
    assert caretaker.get_current_memento() == memento2

    assert caretaker.redo() == memento3
    assert caretaker.get_current_memento() == memento3

    # Undo to initial state
    assert caretaker.undo() == memento2
    assert caretaker.undo() == memento1
    assert caretaker.undo() == memento1  # Should stay at the initial state

    # Redo to the latest state
    assert caretaker.redo() == memento2
    assert caretaker.redo() == memento3
    assert caretaker.redo() is None  # Should stay at the latest state

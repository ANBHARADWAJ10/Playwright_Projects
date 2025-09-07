from playwright.sync_api import sync_playwright
import time


def set_delivery_time(page, delivery_time):
    page.fill("//input[@name='delivery']", delivery_time)
    print(f"✅ Time set to: {delivery_time}")

def basic_search_automation():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        try:
            print("🚀 Starting basic web automation...")

            # Navigate to the webiste
            page.goto("https://httpbin.org/forms/post")

            # Fill out a simple form
            page.type("//input[@name='custname']", "Nikhil")
            page.type("//input[@type='tel']","7036618647")
            page.type("//input[@type='email']","nihkil@gmail.com    ")
            page.type("//textarea[@name='comments']","Playwright")

            # Select from dropdown
            pizza_size = page.locator("//label[text() = ' Small ']")
            pizza_size.click()
            page.wait_for_timeout(3000)
            # page.select_option('select[name="size"]', 'large')



            # Check a checkbox
            page.check('input[name="topping"][value="bacon"]')

            # Time
            delivery_time = "12:15"
            # capture_validation_message(page, delivery_time)
            set_delivery_time(page, delivery_time)

            # Click submit button
            page.click("//button[text()='Submit order']")

            # Wait for navigation and verify we're on results page
            page.wait_for_url("**/post")

            # Basic assertion - check if our data appears in the response
            page_content = page.content()
            assert 'Nikhil' in page_content
            assert '7036618647' in page_content, 'Number not found'

            print("✅ Form submission successful!")
            print("📄 Response received and validated")


            # Take a screenshot for verification
            page.screenshot(path='tmp_scrnsts/form_submission.png')
            print("📸 Screenshot saved as 'form_submission.png'")

        except Exception as e:
            print(f"❌ Error occurred: {e}")
            page.screenshot(path="tmp_scrnsts/error_screenshot.png")

        finally:
            browser.close()


def capture_validation_message(page,delivery_time):
    """
    Capture and print HTML5 validation popup message
    """
    # Fill invalid time to trigger validation popup
    set_delivery_time(page, delivery_time)

    # Try to submit or trigger validation
    page.click("//button[text()='Submit order']")  # or whatever triggers validation

    # Get the validation message
    validation_message = page.evaluate('''
        () => {
            const input = document.querySelector('input[name="delivery"]');
            return input.validationMessage;
        }
    ''')

    if validation_message:
        print(f"🚨 Validation Message: {validation_message}")
    else:
        print("✅ No validation message found")


if __name__ == '__main__':
    basic_search_automation()